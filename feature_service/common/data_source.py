import os
import random
import shutil
from concurrent.futures import as_completed, ThreadPoolExecutor
from typing import (
    List,
    Set,
)

from feature_service.feature_set.annotation import annotate_text, add_annotations
from feature_service.jobs.job_metadata import Subdivisions
from text2phenotype.common import common
from text2phenotype.common.data_source import DataSource, DataSourceContext
from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.common.log import operations_logger
from text2phenotype.constants.features import FeatureType


class FeatureServiceDataSource(DataSource):
    def ann(self, file, feature_types, orig_dir, subdivisions, split_data, ):
        try:
            operations_logger.info(f'Annotating text: {file}')
            featureset = annotate_text(common.read_text(file), feature_types, max_token_size=self.max_token_count)
            featureset_file = file[:-3] + 'json'
            self.save_feature_set_annotations(featureset.to_dict(), featureset_file, orig_dir, subdivisions, split_data=split_data)
        except Exception:
            operations_logger.exception(f'Annotate text failed for file: {file}')

    def feature_set_annotate(self, feature_types: List[FeatureType] = None, subdivisions: Subdivisions = None,
                             split_data: bool = True) -> List[str]:
        """
        this function does featureset annotation on all the original raw text
        """
        futures = []
        executor = ThreadPoolExecutor(1)   # TODO: configure via env variable
        counter = 0
        for orig_dir in self.original_raw_text_dirs:
            file_list = self.get_original_raw_text_files(orig_dir=orig_dir)
            subdivisions.create_subdivision_expect_doc_count(len(file_list))
            operations_logger.info('Starting feature set annotations...')
            for file in file_list:
                f = executor.submit(self.ann, file, feature_types, orig_dir, subdivisions, split_data)
                futures.append(f)
                counter += 1
                if counter >= 100:
                    counter = 0
                    executor.submit(self.sync_features)

        for f in as_completed(futures):
            exc = f.exception()
            if exc:
                operations_logger.error(exc)
        executor.shutdown()
        self.sync_features()
        operations_logger.info('Feature set annotation complete!')
        return []

    def combined_fs_subfolder_paths(self, fs_version: None, context: DataSourceContext = DataSourceContext.train):
        feat_version = fs_version or self.feature_set_version
        subfolders = self.feature_set_subfolders_from_context(context=context)
        return [os.path.join(feat_version, subfold) for subfold in subfolders]

    def text_from_fs_json(self, fs_file, use_old):
        if use_old:
            fs_version = self.old_feature_set_version
        else:
            fs_version = self.feature_set_version
        for fold in self.combined_fs_subfolder_paths(fs_version):
            fold_path = f"/{fold.strip('/')}/"
            if fold_path in fs_file:
                text_file = fs_file.replace(fold_path, '')
                break
        else:
            text_file = fs_file.replace(fs_version, '')
        return text_file

    def get_text_and_feature_set_files(self, original_text_dir: str = None,
                                       get_old_feature_annotations: bool = False) -> List[tuple]:
        text_files = self.get_original_raw_text_files(orig_dir=original_text_dir)
        self.get_feature_set_annotation_files(orig_dir=original_text_dir)
        if get_old_feature_annotations:
            self.get_feature_set_annotation_files(orig_dir=original_text_dir,
                                                  get_old=get_old_feature_annotations)

        already_exists = 0
        matched_files = list()
        for text_file in text_files:
            dest_fs_file = self.get_fs_annotation_from_text_file(text_file, original_text_dir=original_text_dir)
            # if the file already exists within any subfolder of self.feature_set_version, do not include
            if dest_fs_file:
                already_exists += 1
                continue

            # get the old feature set #TODO: utilize this function in annotate not just update_features
            fs_file = self.get_fs_annotation_from_text_file(
                text_file, original_text_dir=original_text_dir, get_old=get_old_feature_annotations)
            # if there's an old fs file or we want to annotate previously unannotated files, append information
            if fs_file or self.annotate_new_files:
                matched_files.append((text_file, fs_file))

        operations_logger.info(f"{already_exists} files found with matching fs annotation in {self.feature_set_version}")
        return matched_files

    def get_fs_annotation_from_text_file(self, text_file, original_text_dir: str, get_old: bool = False):
        if get_old:
            fs_version = self.old_feature_set_version
        else:
            fs_version = self.feature_set_version
        for subfolder in self.feature_set_subfolders:
            fs_dir = os.path.join(fs_version, subfolder, original_text_dir)
            fs_file = text_file.replace(f'/{original_text_dir}/', f'/{fs_dir}/').replace(self.TEXT_SUFFIX,
                                                                                         self.MACHINE_ANNOTATION_SUFFIX)
            if os.path.isfile(fs_file):
                return fs_file
        operations_logger.info(f'Failed to find fs file for text file: {text_file}')

    def update_ann(self, fs_path, text_path, features_for_update):
        # if the file has previously been annotated and exists locally
        if fs_path is not None and os.path.isfile(fs_path):
            if os.stat(fs_path).st_size > 500 * 1e6:
                operations_logger.info("Old Json > 500 MB, skipping")
                # 500 MB chosen bc otherwise feature service was OOMing and dying, 300k token documents have
                # fs annotation files smaller than this so it's a reasonable threshold
                return

            out_file_path = fs_path.replace(self.old_feature_set_version, self.feature_set_version)
            # if we've listed features to update, update annotations, if left blank just copy the file over
            if len(features_for_update) >= 1:
                old_featureset = common.read_json(fs_path)
                txt = common.read_text(text_path)
                operations_logger.info(f'updating features for file {fs_path}')
                try:
                    featureset = add_annotations(txt,
                                                 MachineAnnotation(
                                                     json_dict_input=old_featureset,
                                                     text_len=len(txt)),
                                                 features_for_update)

                    common.write_json(featureset.to_dict(), out_file_path)
                except:
                    operations_logger.warning(f'Adding features {features_for_update} failed on document {fs_path}')
            # if the features to update are None and feature_set_version != old_feature_set_version,
            # just copy the old file over
            elif out_file_path != fs_path:
                directory = os.path.dirname(out_file_path)
                os.makedirs(directory, exist_ok=True)
                shutil.copy(fs_path, out_file_path)
                operations_logger.info(f"Saving file to {out_file_path}")

    def update_features(self, features_for_update: Set[FeatureType], subdivisions: Subdivisions = None,
                        split_data: bool = False) -> List[str]:
        executor = ThreadPoolExecutor(1)    # TODO: configure as env variable
        counter = 0
        futures = []
        failed_files = []
        operations_logger.info(
            f'Starting Updating Annotations with "annotate_new_files": {self.annotate_new_files}')
        for orig_dir in self.original_raw_text_dirs:
            matched_files = self.get_text_and_feature_set_files(original_text_dir=orig_dir,
                                                                get_old_feature_annotations=True)
            if self.annotate_new_files and split_data:
                subdivisions.create_subdivision_expect_doc_count(len(matched_files))
                operations_logger.info(f'subdivision keys : {subdivisions.subdivision_probs.keys()}')
                # reduce the subdivision count for all files that already exist in the current folder so that after
                # updating they will be evenly distributed, this solves for prior annotations that were unevenly split
                for i in matched_files:
                    if i[1] is not None:
                        for cat in subdivisions.subdivision_probs.keys():
                            if f'/{cat}' in i[1]:
                                subdivisions.reduce_exp_doc_count(cat)
                                operations_logger.debug(f'reducing subdivision count for {cat}, fp: {matched_files[1]}')
                operations_logger.info(f"Using subdivisions: {subdivisions.subdivision_doc_count}")

            total_orig = len(matched_files)
            matched_file_count = len([f for f in matched_files if f[1]])
            operations_logger.info(f'Updating Annotations: # of matched files {matched_file_count},'
                                   f' # unmatched: {total_orig - matched_file_count}')
            for fps in matched_files:
                text_path = fps[0]
                fs_path = fps[1]
                # if the file has previously been annotated and exists locally
                if fs_path is not None and os.path.isfile(fs_path):
                    future = executor.submit(self.update_ann, fs_path, text_path, features_for_update)
                # otherwise if we've specified we want to annotate new files, annotate new files (with all featuerss_
                elif self.annotate_new_files:
                    future = executor.submit(self.ann, common.read_text(text_path), None, orig_dir, subdivisions, split_data)
                futures.append(future)
                counter += 1
                if counter >= 100:
                    counter = 0
                    executor.submit(self.sync_features)

        executor.shutdown()
        self.sync_features()
        operations_logger.info('Feature set annotation complete!')
        return failed_files

    def sync_features(self):
        local_path = os.path.join(self.parent_dir, self.feature_set_version)
        folder = os.path.join(self.feature_set_version)
        self.sync_up(local_path, folder.replace(self.parent_dir, '').lstrip('/'))

    def save_feature_set_annotations(self, contents: dict,
                                     original_file_path: str,
                                     orig_dir: str = None,
                                     subdivisions: Subdivisions = None,
                                     split_data: bool = True):
        feature_set_dir = os.path.join(self.parent_dir, self.feature_set_version)
        # train will be parent/feature_set_version/train
        # test will be parent/feature_set_version/test
        if split_data:
            if not orig_dir:
                operations_logger.info('No orig_dir provided and trying to split data')
            else:
                prob = random.uniform(0, 1)
                for entry in subdivisions.subdivision_split_points:
                    prob_range_for_folder = subdivisions.subdivision_split_points[entry]
                    if prob_range_for_folder[0] <= prob < prob_range_for_folder[1]:
                        feature_set_dir = os.path.join(feature_set_dir, entry)
                        subdivisions.reduce_exp_doc_count(entry)
                        break
                else:
                    operations_logger.info(
                        f'NO subdivision found for prob: {prob} with subdivisions: '
                        f'{subdivisions.default_subdivision_probs} with  split points '
                        f'{subdivisions.subdivision_split_points}')

        absolute_file_path = original_file_path.replace(self.parent_dir, feature_set_dir)
        operations_logger.info(f"Saving Feature Set annotation to {absolute_file_path}")
        common.write_json(contents, absolute_file_path)
        return subdivisions

    @staticmethod
    def update_file_path(absolute_file_path, sub_dir):
        path, file_name = os.path.split(absolute_file_path)
        return os.path.join(path, sub_dir, file_name)
