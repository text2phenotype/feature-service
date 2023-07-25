from collections import defaultdict
from itertools import chain
import os
from typing import List, Tuple
from collections import Counter

import pandas as pd

from text2phenotype.common import common
from text2phenotype.common.log import operations_logger
from text2phenotype.constants.features.label_types import ProblemLabel

from feature_service.common.data_source import FeatureServiceDataSource
from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.jobs.job_metadata import JobMetadata

# amount of allowable difference in start and end ranges for a labeled token
OVERLAP_THRESHOLD = 2

# how many characters before and after a label range
CONTEXT_CHAR_LEN = 40


class AnnotatorDisagreement:
    FILE_KEY = 'base_file'
    RANGE_KEY = 'range'
    TEXT_KEY = 'text'
    CONTEXT_KEY = 'context'
    NA_LABEL = "na"

    def __init__(self, data_source: FeatureServiceDataSource, job_metadata: JobMetadata):
        self.data_source = data_source
        self.job_metadata = job_metadata
        self.annotation_overlap = None
        self.text_to_ann_name_dict = None

    @staticmethod
    def split_brat_words(text, text_range, label):
        # split brat annotations into individual word annotations so as to treat highlighting individual words
        # the same as highlighting the whole phrase
        output = []
        space_split = text.split()
        start_index = 0
        for token in space_split:
            temp_text = token
            span = text.find(temp_text, start_index)
            temp_range = (text_range[0] + span, text_range[0] + span + len(temp_text))
            start_index = span + len(temp_text)
            output.append([temp_range, temp_text, label])
        return output

    def parse_brat_to_positions(self, file):
        # takes as input a ann file and outputs a list of lists of the format [(range0, range1), text, label]
        output = []
        parsed_brat = FeatureServiceDataSource.parse_brat_ann_with_link_info(file)
        for annotation in parsed_brat:
            aspect = parsed_brat[annotation].label.lower()
            if aspect == ProblemLabel.problem.name:
                aspect = ProblemLabel.diagnosis.name

            if self.job_metadata.annotator_categories and aspect not in self.job_metadata.annotator_categories:
                continue

            output.extend(self.split_brat_words(parsed_brat[annotation].text,
                                                parsed_brat[annotation].text_range,
                                                aspect))

        return sorted(output, key=lambda x: x[0])

    def get_mapping_base_to_all_annotators(self):
        # given ann_dirs and original_raw_text within the datasource
        # maps all the base original text files to full annotation paths

        ann_files = self.data_source.get_ann_files()
        self.data_source.get_original_raw_text_files()  # sync down

        if len(self.data_source.ann_dirs) < 2:
            raise ValueError("You cannot compare inter-annotator disagreement with less than two sets of anns")
        file_dict = defaultdict(list)
        # get a dictionary of original_raw_text path : list of anns that matched that

        for file in ann_files:
            text_filename = self.data_source.get_text_from_ann_file(file)
            if text_filename:
                file_dict[text_filename].append(file)
        operations_logger.info(f'File mapping created with {len(file_dict.keys())} entries')
        return file_dict

    @staticmethod
    def check_small_range_diff(range_1, range_2):
        # boolean method to confirm that there is not a large region of text in one range that's not in the other,
        # allows for loose logic on whether two ranges are the same
        return abs(range_2[0] - range_1[0]) < OVERLAP_THRESHOLD and abs(range_2[1] - range_1[1]) < OVERLAP_THRESHOLD

    def get_annotator_name(self, fp):
        # gets the ann_dir name out of the file path given the base original raw text information
        for ann_dir in self.data_source.ann_dirs:
            if ann_dir in fp:
                return ann_dir

    @staticmethod
    def check_pointers_position(positions, pointers):
        """Return true if any pointers have not reached the end of the associated positions list"""
        return any([pointers[i] < len(positions[i]) for i in range(len(pointers))])

    @classmethod
    def write_row(cls, entry: list, annotator_name: str, file_id: str = None, text: str = None):
        """Create row for each annotation entry"""
        # TODO(mjp): this may not be returning the correct context, see annotator_disagreement.csv output
        context = ''
        if text:
            context = text[max(0, entry[0][0] - CONTEXT_CHAR_LEN): entry[0][1] + CONTEXT_CHAR_LEN].replace("\n", " ")
        row = {
            cls.FILE_KEY: file_id,
            annotator_name: entry[2],
            cls.TEXT_KEY: entry[1],
            cls.RANGE_KEY: entry[0],
            cls.CONTEXT_KEY: context,
        }
        return row

    @staticmethod
    def check_overlap(rng1, rng2):
        # boolean to check if two ranges overlap
        return rng1[0] <= rng2[1] and rng2[0] <= rng1[1]

    @classmethod
    def get_overlap_doc(
            cls,
            positions:  List[List[list]],
            pointers: list,
            ann_fps: List[str],
            txt: str = None,
            file_id: str = None
    ) -> dict:
        """
        For a raw text file and set of annotations, identify which annotations overlap

        :param positions: List[List[List[Tuple, str, str]]]
            Outer list is for each annotator
            second list is for each annotation
            third list contains (start, end, text, label)
            eg:
            [[[(259, 263), 'type', 'diagnosis'], [(264, 265), 'I', 'diagnosis'], ...]
        :param pointers: List[int]
        :param ann_fps: List of annotation  file paths
        :param orig_text_fp: str
            file path to the referenced original text
        :returns: dict
            A dict with the raw text filename, the annotators, the text, the range, the context,
            and what label each annotator gave.
            If an annotator did not give a label for the token, 'NA' is given.
        """
        # positions must be sorted before calling the rest of this method
        rows = []
        num_pointers = len(pointers)

        while cls.check_pointers_position(positions, pointers):
            entries = [None] * num_pointers
            text_ranges = []
            for p in range(num_pointers):
                if pointers[p] < len(positions[p]):
                    entries[p] = positions[p][pointers[p]]
                    text_ranges.append(entries[p][0])
                else:
                    entries[p] = None
            min_range = min(text_ranges)
            for j in range(len(pointers)):
                # find the min range of all entries at that point in time
                if entries[j] and cls.check_overlap(entries[j][0], min_range):
                    pointers[j] += 1
                    # loop through all other entries
                    row = cls.write_row(entries[j], annotator_name=ann_fps[j], file_id=file_id, text=txt)
                    for h in chain(range(0, j), range(j + 1, len(pointers))):
                        # check that entry[h] follows entry format
                        # (otherwise could correspond to empty lines at end of file) and check that the entries overlap
                        # and that the text is the same

                        if entries[h] and cls.check_overlap(entries[j][0], entries[h][0]) and \
                                cls.check_small_range_diff(entries[j][0], entries[h][0]):
                            row[ann_fps[h]] = entries[h][2]
                            pointers[h] += 1
                            row['different'] = entries[h][2] != entries[j][2]
                        else:
                            row[ann_fps[h]] = cls.NA_LABEL
                            row['different'] = True

                    rows.append(row)
                    break
        return rows

    @classmethod
    def combine_adjacent_label_tokens(cls, annotation_overlap_df: pd.DataFrame, ann_dirs: List[str]) -> pd.DataFrame:
        """
        Combine adjacent tokens that have the same label
        Expected to only have the class key labels
        """
        df = annotation_overlap_df.copy()
        file_indices = defaultdict(list)
        for row_index, row in df.iterrows():
            file_indices[row[cls.FILE_KEY]].append(row_index)

        if not len(file_indices):
            return pd.DataFrame()

        indices_to_remove = set()
        for indices in file_indices.values():
            indices = sorted(indices, key=lambda x: df.loc[x, cls.RANGE_KEY])

            i = 0
            while i < len(indices) - 1:
                token_1 = df.loc[indices[i]].copy()  # copy avoids SettingWithCopyWarning
                range_1 = token_1.loc[cls.RANGE_KEY]
                token_2 = df.loc[indices[i + 1]]
                range_2 = token_2.loc[cls.RANGE_KEY]

                # combine adjacent annotations
                if range_1[1] == range_2[0] - 1:
                    for ann_dir in ann_dirs:
                        token_1.loc[ann_dir] += ',' + str(token_2.loc[ann_dir])

                    token_1.loc[cls.TEXT_KEY] += ' ' + str(token_2.loc[cls.TEXT_KEY])
                    token_1.loc[cls.CONTEXT_KEY] += token_2[cls.CONTEXT_KEY][-(len(token_2.loc[cls.TEXT_KEY]) + 1):]
                    token_1.loc[cls.RANGE_KEY] = (range_1[0], range_2[1])
                    df.loc[indices[i]] = token_1  # set the updated token row with new values

                    indices_to_remove.add(indices[i + 1])
                    # deleting the element works because i doesnt increment in this branch of the loop
                    del indices[i + 1]
                else:
                    i += 1

        operations_logger.info(f'Removing a total of {len(indices_to_remove)} redundant rows.')

        df.drop(list(indices_to_remove), inplace=True)
        return df

    @staticmethod
    def get_labels(annotation_df, ann_dirs):
        """
        annotation_df must have columns with ann_dirs as titles,
        where each column has the various possible annotations
        """
        return sorted(list(set(annotation_df[ann_dirs].values.ravel())))

    def annotator_voting(self, text_to_ann_name_dict: dict):
        """
        Given a dict of annotation files for each raw text file, return
        """
        ann_dirs = self.data_source.ann_dirs.copy()
        n_annotators = len(ann_dirs)
        # input dict should be of format annotator_name: sorted list of lists (range, text , aspect)
        cols = [self.RANGE_KEY, self.TEXT_KEY, self.CONTEXT_KEY, self.FILE_KEY, 'different']
        cols.extend(ann_dirs)
        all_annotation_overlaps = []
        for base_file, annotated_fps in text_to_ann_name_dict.items():
            annotators = []
            positions = []
            if len(annotated_fps) <= 1:
                continue

            for file in annotated_fps:
                positions.append(self.parse_brat_to_positions(file))
                annotators.append(self.get_annotator_name(file))
            pointers = [0] * len(annotated_fps)
            overlap_pos = self.get_overlap_doc(
                positions,
                pointers=pointers,
                ann_fps=annotators,
                file_id=base_file,
                txt=common.read_text(base_file)
            )
            if overlap_pos:
                all_annotation_overlaps.extend(overlap_pos)
        annotation_overlap_df = pd.DataFrame(all_annotation_overlaps, columns=cols)
        annotation_overlap_df = annotation_overlap_df.fillna(self.NA_LABEL)

        # get votes for each label
        labels = self.get_labels(annotation_overlap_df, ann_dirs)
        votes_df = pd.concat([(annotation_overlap_df[ann_dirs] == label).sum(axis=1) for label in labels], axis=1)
        votes_df.columns = [f"votes_{label}" for label in labels]
        annotation_overlap_df = annotation_overlap_df.join(votes_df)

        # Get agreement for each non-na label (num votes over target and na is the total number of votes available)
        # Assumes that if there is at least one positive vote and all positive votes are saying the same thing,
        # then we say that the annotators agree on the token labels.
        # NOTE: this includes matches with punctuation, eg `,` or `-`, which are common labeled tokens, adding noise
        agree_df = pd.DataFrame({
            f"is_{label}": annotation_overlap_df[f"votes_{label}"] == n_annotators
            for label in labels
        })
        agree_df["pos_disagree"] = ~agree_df.any(axis=1) # no one agrees on the positive label
        annotation_overlap_df = annotation_overlap_df.join(agree_df)

        self.annotation_overlap = annotation_overlap_df
        return annotation_overlap_df

    def _disagree_ratio_by_file(self, annotation_overlap_df, by_key="different"):
        """Find mismatch ratio for each text file in dataframe"""
        file_groups = annotation_overlap_df.groupby(self.FILE_KEY)
        disagree_ratio = file_groups[by_key].agg(['count', 'sum'])
        disagree_ratio['overlap_ratio'] = 1 - disagree_ratio['sum'] / disagree_ratio['count']
        disagree_ratio.columns = ['Count Tokens', 'Count Tokens In Conflict', 'all_agree ratio']
        disagree_ratio.astype({'Count Tokens In Conflict': int})  # make sure counts are integers, not float or bool
        return disagree_ratio

    def write_reports(self, iaa_summary, combined_tokens_diff_df, combined_pos_tokens_diff_df, pos_mismatch_ann_df,
                      disagree_ratio, pos_disagree_ratio):
        """Write out the reports"""
        base_path = os.path.join(FeatureServiceEnv.DATA_ROOT.value, self.job_metadata.job_id)

        common.write_json(iaa_summary, os.path.join(base_path, 'iaa_summary.json'))
        disagree_ratio.to_csv(os.path.join(base_path, 'overlap_ratio.csv'))
        pos_disagree_ratio.to_csv(os.path.join(base_path, 'positive_disagree_ratio.csv'))
        combined_tokens_diff_df.to_csv(os.path.join(base_path, 'annotator_disagreement.csv'))
        pos_mismatch_ann_df.to_csv(os.path.join(base_path, 'positive_disagreement_full.csv'))
        combined_pos_tokens_diff_df.to_csv(os.path.join(base_path, 'positive_disagreement_concat.csv'))

        operations_logger.info(f"Wrote report files to: {base_path}")

    def annotator_disagreement(self):
        """
        For any set of annotators will return a data table with all the phrases/ranges that annotators voted on.
        """
        self.text_to_ann_name_dict = self.get_mapping_base_to_all_annotators()  # sync files down & get filename map
        num_matched_text_files = len(self.text_to_ann_name_dict)

        # collect annotation sources, then the add'l info colums
        ann_dirs = self.data_source.ann_dirs.copy()
        cols = ann_dirs + [self.TEXT_KEY, self.CONTEXT_KEY, self.FILE_KEY, self.RANGE_KEY]

        # complete list of tokens and annotations. Use this as base for creating all other analysis & reports
        annotation_overlap_df = self.annotator_voting(self.text_to_ann_name_dict)

        # report how many individual tokens arent labeled the same, including missed "na" tokens
        disagree_ratio = self._disagree_ratio_by_file(annotation_overlap_df)
        mean_agree_ratio = disagree_ratio['all_agree ratio'].mean()
        weighted_mean_agree_ratio = (
                (disagree_ratio['all_agree ratio'] * disagree_ratio['Count Tokens']).sum()
                / disagree_ratio['Count Tokens'].sum()
        )

        # how many tokens were voted on by more than one annotator and don't match
        pos_disagree_ratio = self._disagree_ratio_by_file(annotation_overlap_df, by_key="pos_disagree")
        mean_pos_agree_ratio = pos_disagree_ratio['all_agree ratio'].mean()
        weighted_mean_pos_agree_ratio = (
                (pos_disagree_ratio['all_agree ratio'] * pos_disagree_ratio['Count Tokens']).sum()
                / pos_disagree_ratio['Count Tokens'].sum()
        )

        # get table with just the positive mismatches (ignores any 'na' mismatches)
        pos_mismatch_ann_df = annotation_overlap_df[annotation_overlap_df["pos_disagree"]][cols]
        ratio_pos_mismatch = pos_mismatch_ann_df.shape[0] / annotation_overlap_df.shape[0]
        combined_pos_tokens_diff_df = self.combine_adjacent_label_tokens(pos_mismatch_ann_df, self.data_source.ann_dirs)

        # get all labels that don't match (incl na) and join adjacent labels for report
        different_annotations_df = annotation_overlap_df[annotation_overlap_df.different][cols]
        ratio_mismatch = different_annotations_df.shape[0] / annotation_overlap_df.shape[0]
        combined_tokens_diff_df = self.combine_adjacent_label_tokens(different_annotations_df,
                                                                     self.data_source.ann_dirs)

        # get summary data
        iaa_summary = {
            "ann_dirs": ann_dirs,
            "total_count_positive_mismatches": pos_mismatch_ann_df.shape[0],
            "total_token_mismatch_ratio": ratio_mismatch,
            "total_positive_token_mismatch_ratio": ratio_pos_mismatch,
            "count_labeled_tokens": annotation_overlap_df.shape[0],
            "count_txt_files": num_matched_text_files,
            "mean_agree_ratio": mean_agree_ratio,
            "weighted_mean_agree_ratio": weighted_mean_agree_ratio,
            "mean_pos_agree_ratio": mean_pos_agree_ratio,
            "weighted_mean_pos_agree_ratio": weighted_mean_pos_agree_ratio,
        }
        operations_logger.info(
            f"Of {annotation_overlap_df.shape[0]} labeled tokens in {num_matched_text_files} files, "
            f"{ratio_pos_mismatch * 100:.3f}% ({pos_mismatch_ann_df.shape[0]}) of positive tokens were mismatched")

        # write out reports
        self.write_reports(iaa_summary, combined_tokens_diff_df, combined_pos_tokens_diff_df, pos_mismatch_ann_df,
                           disagree_ratio, pos_disagree_ratio)

    @staticmethod
    def highest_vote_label_list(label_list: list) -> List[Tuple[str, int]]:
        """
        Return the label(s) with the highest frequency from list of labels
        output is list of single or multiple matches for highest frequency, eg
            ['diagnosis'] or ['diagnosis', 'signsymptom'] if votes are tied
        """
        votes_dict = dict(Counter(label_list))
        highest_votes = [k for k, v in votes_dict.items() if v == max(votes_dict.values())]
        return highest_votes

    @classmethod
    def vote(cls, annotation_row, ann_dirs, annotator_total_token_counts, labels_no_na):
        """
        Core method for handling annotator disagreements

        If annotators already agree on a label, return that label
        If annotators disagree:
            - If single token in label, find the positive label with the most votes
                - If one label with most votes, return that label
                - If multiple positive labels with max votes, return label from annotator with most labeled tokens
            - If multiple tokens in label (separated by ","), find the positive label with the most votes
                - if one label has most votes, return that label
                - if multiple positive labels, collapse joined labels to single label, & return highest trust label
                    -if joined label has multiple positive labels ('signsymptom,diagnosis,diagnosis'), we ignore it
        """
        # check if we already have labeler agreement first, get the label if matching col is true
        matched_label = [labl for labl in labels_no_na if annotation_row.loc[f"is_{labl}"]]
        label_out = None
        if len(matched_label) == 1:
            label_out = matched_label[0]
        elif annotation_row["pos_disagree"]:  # len(matched_label) should be zero here
            # do voting procedure
            if "," not in annotation_row[ann_dirs[0]]:
                highest_vote = cls.highest_vote_label_list([token_labels for token_labels in annotation_row[ann_dirs]])
                if len(highest_vote) == 1:
                    label_out = highest_vote[0]
                else:
                    # if a simple match, and votes are tied, use the person who labeled more from non-na labels
                    # remove any labelers with "na"
                    positive_annotators = annotator_total_token_counts[
                        annotation_row[ann_dirs] != cls.NA_LABEL]
                    label_out = annotation_row[positive_annotators.idxmax()]
            else:
                # we get something like this
                # annotations/anne.frea                          signsymptom,na,signsymptom,na,na
                # annotations/satjiv.kohli      diagnosis,diagnosis,diagnosis,diagnosis,diagnosis
                # annotations/despina.siolas            signsymptom,signsymptom,signsymptom,na,na
                votes_dict = [
                    dict(Counter(token_labels.split(",")))
                    for token_labels in annotation_row[ann_dirs]]
                collapse_pos_labels = [k for vote in votes_dict for k in vote if k != AnnotatorDisagreement.NA_LABEL]
                highest_vote = cls.highest_vote_label_list(collapse_pos_labels)
                if len(highest_vote) == 1:
                    label_out = highest_vote[0]
                else:
                    # joined keys tied, find voting labels & associated labeler trust
                    # ignore any "na" labels or joined labels with more than one positive label
                    vote_keys = [[k for k in vote.keys() if k != AnnotatorDisagreement.NA_LABEL] for vote in votes_dict]
                    label_with_trust = [
                        (v[0], c) if len(v) == 1 else (None, 0)
                        for v, c in zip(vote_keys, annotator_total_token_counts.values)]
                    label_out = max(label_with_trust, key=lambda y: y[1])[0]
        else:
            # if matched_label is empty and pos_disagree is false, we don't have a clear winner
            msg = f"voting got to an unstable logic point; check the content\n {annotation_row}"
            operations_logger.error(msg)
            label_out = cls.NA_LABEL
        return label_out
