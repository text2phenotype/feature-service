import argparse
import datetime
import os
import time

import pandas as pd

from text2phenotype.common import common
from text2phenotype.common.log import operations_logger
from text2phenotype.constants.environment import Environment
from text2phenotype.constants.features.label_types import list_annotation_labels, SignSymptomLabel, ProblemLabel
from text2phenotype.annotations.file_helpers import AnnotationSet
from feature_service import RESULTS_PATH
from feature_service.active.annotator_disagreement import AnnotatorDisagreement
from feature_service.common.data_source import FeatureServiceDataSource
from feature_service.jobs.job_metadata import JobMetadata

RUN_PROFILE = False

# TARGET_FILE = "/Users/michaelpesavento/Documents/model_train_params/iaa_20201009/i2b2_demographics_iaa_20201006_test.json"
TARGET_FILE = "/Users/michaelpesavento/Documents/model_train_params/iaa_20201009/diseasesign_phi_iaa_20201005.json"

# is there a better way to get the label_type class from a label string?
# Annotation.category_label_from_enum_label_name finds first match, but this is often the incorrect match
LABEL_CATEGORY_MAP = {
    'diagnosis': ProblemLabel.get_category_label().persistent_label,
    'signsymptom': SignSymptomLabel.get_category_label().persistent_label,
}

# what name do we use for the merged dataset?
LABEL_SET_NAME = "diagnosis_sign"


def set_pd_display():
    pd.options.display.width = 300
    pd.set_option("max_columns", None)


def main():
    script_start_time = time.time()
    parser = argparse.ArgumentParser(description="Load job metadata")
    parser.add_argument(
        "metadata_filename", type=str, nargs="?", default=TARGET_FILE,
        help="filename for json job metadata")
    args = parser.parse_args()

    parameters_dict = common.read_json(args.metadata_filename)['metadata']
    data_source = FeatureServiceDataSource(**parameters_dict)
    job_metadata = JobMetadata(**parameters_dict)

    disagreement = AnnotatorDisagreement(data_source=data_source, job_metadata=job_metadata)
    disagreement.annotator_disagreement()

    annotation_overlap_df = disagreement.annotation_overlap
    filename_map = disagreement.text_to_ann_name_dict
    ann_dirs = disagreement.data_source.ann_dirs.copy()

    combined_annotations_df = disagreement.combine_adjacent_label_tokens(
        annotation_overlap_df, ann_dirs)

    # count the number of tokens for each annotator across the whole dataset
    labels = sorted(list(set(annotation_overlap_df[ann_dirs].values.ravel())))
    labels_no_na = [x for x in labels if x != disagreement.NA_LABEL]
    n_labels_df = pd.concat([(annotation_overlap_df[ann_dirs] == label).sum(axis=0) for label in labels_no_na], axis=1)
    n_labels_df.columns = labels_no_na
    # use this for tiebreaks, with identifying which annotator has more tokens
    annotator_total_token_counts = n_labels_df.sum(axis=1)

    output_base_path = os.path.join(
        disagreement.data_source.parent_dir,
        "annotations",
        f"gold_{LABEL_SET_NAME}"
    )

    # loop over combined annotations per file & create list
    for text_fn, ann_files in filename_map.items():
        cur_ann_df = combined_annotations_df[combined_annotations_df.base_file == text_fn]
        ann_set = AnnotationSet()

        # skip writing out any annotation files that dont have any annotations
        if cur_ann_df.empty:
            operations_logger.debug(f"No annotations found for file: {text_fn}")
            continue

        for ix, row in cur_ann_df.iterrows():
            label_out = AnnotatorDisagreement.vote(row, ann_dirs, annotator_total_token_counts, labels_no_na)

            ann_set.add_annotation_no_coord(
                label=label_out,
                text_range=row["range"],
                text=row["text"]
            )

        dataset_path = os.path.relpath(text_fn, disagreement.data_source.parent_dir)
        output_ann_path = os.path.join(
            output_base_path,
            os.path.splitext(dataset_path)[0] + ".ann"
        )
        os.makedirs(os.path.dirname(output_ann_path), exist_ok=True)
        common.write_text(ann_set.to_file_content(), output_ann_path)
        operations_logger.debug(f"Writing annotation file: {output_ann_path}")

    print(f"Total run time: {time.time() - script_start_time:0.3f} seconds")


def profile_func(my_func):
    """Used in creating cProfiled output for the main() function"""
    import cProfile
    import pstats
    import io

    pr = cProfile.Profile()
    pr.enable()

    # call the function
    my_func()

    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats()

    timestamp = datetime.datetime.now().strftime("%Y%d%m_%H%M%S")
    with open(os.path.join(RESULTS_PATH, f'profile_stats_{timestamp}.txt', 'w+')) as f:
        f.write(s.getvalue())


if __name__ == "__main__":
    set_pd_display()
    Environment.load()
    if RUN_PROFILE:
        profile_func(main())
    else:
        main()
