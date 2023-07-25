from collections import defaultdict
import csv
import os
from typing import Dict, List, Set, Tuple

from feature_service.common.data_source import FeatureServiceDataSource
from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.jobs.job_metadata import JobMetadata

from text2phenotype.common.common import read_json
from text2phenotype.common.log import operations_logger


class ApiDisagreement:
    __RESULT_FILES_KEY = 'results'
    __SOURCE_DOC_KEY = 'source'

    """Create disagreement reports for outputs from API calls."""
    def __init__(self, data_source: FeatureServiceDataSource, job_metadata: JobMetadata):
        self.data_source = data_source
        self.job_metadata = job_metadata

    def disagreement(self):
        if len(self.data_source.ann_dirs) != 2:
            raise ValueError("API disagreement must be computed between 2 sets of annotations.")

        job1_files = self.__get_job_files(self.data_source.ann_dirs[0])
        operations_logger.info(f"Found {len(job1_files)} job1 files.")
        job2_files = self.__get_job_files(self.data_source.ann_dirs[1])
        operations_logger.info(f"Found {len(job2_files)} job2 files.")

        matched_files = self.__pair_job_files(job1_files, job2_files)
        operations_logger.info(f'Matched {len(matched_files)} files.')

        diffs = self.__get_annotation_diffs(matched_files)

        self.__generate_report(diffs)

    @classmethod
    def __get_annotation_diffs(cls, matched_files: List[str]) -> List[Tuple]:
        differences = list()

        for f1, f2 in matched_files:
            ann1 = read_json(f1)
            ann2 = read_json(f2)

            unique1 = cls.__get_unique_terms(ann1)
            unique2 = cls.__get_unique_terms(ann2)

            types = unique1.keys() | unique2.keys()
            for ann_type in types:
                terms1 = unique1.get(ann_type, set())
                terms2 = unique2.get(ann_type, set())

                differences.extend((f1, f2, ann_type, x, '') for x in terms1 - terms2)
                differences.extend((f1, f2, ann_type, '', x) for x in terms2 - terms1)

        return differences

    @staticmethod
    def __get_unique_terms(annotations: Dict) -> Dict[str, Set]:
        unique = defaultdict(set)

        for key, values in annotations.items():
            for value in values:
                text_key = 0 if isinstance(value, list) else "preferredText"

                unique[key].add(value[text_key].lower())

        return unique

    def __generate_report(self, differences: List[Tuple]):
        report_file = os.path.join(FeatureServiceEnv.DATA_ROOT.value, self.job_metadata.job_id, 'api_disagreement.csv')
        with open(report_file, 'w+') as fh:
            writer = csv.writer(fh)

            writer.writerow([self.data_source.ann_dirs[0],
                             self.data_source.ann_dirs[1],
                             'Aspect', 'Term1', 'Term2'])
            for d in differences:
                writer.writerow(d)

    @classmethod
    def __pair_job_files(cls, job1_files: Dict, job2_files: Dict) -> List[str]:
        job1_map = cls.__get_doc_to_id_map(job1_files)
        job2_map = cls.__get_doc_to_id_map(job2_files)

        doc_ids = job1_map.keys() | job2_map.keys()

        matched_files = []
        for doc_id in doc_ids:
            if doc_id not in job1_map or doc_id not in job2_map:
                continue

            job1_doc_files = job1_files[job1_map[doc_id]][cls.__RESULT_FILES_KEY]
            job2_doc_files = job2_files[job2_map[doc_id]][cls.__RESULT_FILES_KEY]

            job1_endpoint_files = cls.__get_endpoint_map(job1_doc_files)
            job2_endpoint_files = cls.__get_endpoint_map(job2_doc_files)

            for endpoint, fname in job1_endpoint_files.items():
                if endpoint in job2_endpoint_files:
                    matched_files.append((fname, job2_endpoint_files[endpoint]))

        return matched_files

    @classmethod
    def __get_endpoint_map(cls, job_files: List[str]) -> Dict:
        return {cls.__get_endpoint(job_file): job_file for job_file in job_files}

    @staticmethod
    def __get_endpoint(fname) -> str:
        return os.path.basename(fname).split('.')[-2]

    @classmethod
    def __get_doc_to_id_map(cls, job_files: Dict) -> Dict:
        return {file_info[cls.__SOURCE_DOC_KEY]: fid for fid, file_info in job_files.items()}

    def __get_job_files(self, job_dir: str) -> Dict:
        file_map = defaultdict(dict)

        for f in self.data_source.get_files([job_dir], 'json', True):
            fname = os.path.basename(f)
            fid = fname.split('.')[0]
            fid_dict = file_map[fid]

            if f.endswith('annotations.json') or f.endswith('vectorization.json'):
                continue

            if f.endswith('metadata.json'):
                content = read_json(f)
                fid_dict[self.__SOURCE_DOC_KEY] = content['document_info']['source']
            else:
                if self.__RESULT_FILES_KEY not in fid_dict:
                    fid_dict[self.__RESULT_FILES_KEY] = []

                fid_dict[self.__RESULT_FILES_KEY].append(f)

        return file_map
