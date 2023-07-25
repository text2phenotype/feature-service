"""
I2B2 reader for 2010 Relation Challenge dataset
Converts i2b2 annotations to BRAT format, aligns text files

I2B2 / n2c2 NLP research datasets
https://portal.dbmi.hms.harvard.edu/projects/n2c2-nlp/

Annotation file formatting:
https://www.i2b2.org/NLP/Relations/assets/Annotation%20File%20Formatting.pdf
"""
from datetime import datetime
import os
from enum import Enum
import time

from text2phenotype.common import common
from text2phenotype.common.log import operations_logger
from text2phenotype.annotations.i2b2_reader import I2B2Reader, DataContext
from text2phenotype.constants.features.label_types import ProblemLabel
from feature_service.feature_service_env import FeatureServiceEnv


I2B2_2010_DIR = os.path.join('I2B2', '2010 Relation Challenge')
INPUT_ROOT_DIR = os.path.join(FeatureServiceEnv.DATA_ROOT.value, I2B2_2010_DIR)
INSTITUTE_FOLDERS = [
    "beth",  # Beth Israel Deaconess Medical Center
    "partners",  # Partners HealthCare
]


# output folder constants
cur_date = datetime.now().strftime('%Y%m%d')
RELATIVE_OUTPUT_DIR = os.path.join(I2B2_2010_DIR, f"gold_{cur_date}")
OUTPUT_ANNOTATION_ROOT_DIR = os.path.join(
    FeatureServiceEnv.DATA_ROOT.value, "annotations", "diagnosis", RELATIVE_OUTPUT_DIR)
OUTPUT_TEXT_ROOT_DIR = os.path.join(FeatureServiceEnv.DATA_ROOT.value, RELATIVE_OUTPUT_DIR)

BUCKET_NAME = "biomed-data"

# used to strip from ends of text
STOP_PUNCTUATION = ",.:;?!"

# use this for consistent train/test split
SPLIT_RANDOM_SEED = 1234567890


class AnnotationType(Enum):
    """
    Folder divisions for different 2010 annotation types
    """
    assertion = "ast"  # https://www.i2b2.org/NLP/Relations/assets/Assertion%20Annotation%20Guideline.pdf
    concept = "con"  # https://www.i2b2.org/NLP/Relations/assets/Concept%20Annotation%20Guideline.pdf
    relation = "rel"  # https://www.i2b2.org/NLP/Relations/assets/Relation%20Annotation%20Guideline.pdf


class LabelMarkers:
    """
    Markers used in I2B2 2010 relation challenge dataset
    Only concept has token coordinates with the text, format c="coronary artery bypass graft" 115:4 115:7
    """
    concept = "c"  # always followed by token coordinates
    type = "t"  # concept type
    assertion = "a"
    relation = "r"


class ConceptTypeLabels:
    """
    Labels used for distinguishing topics ("t=")
    """
    treatment = "treatment"
    problem = "problem"
    test = "test"


class I2B22010ProblemReader(I2B2Reader):
    """
    Read I2B2 2010 annotation data, convert to brat
    """
    def convert_label_annotation_to_brat(self, target_label: str, i2b2_label: str):
        ann_type = AnnotationType.concept
        concept_type_filter = ConceptTypeLabels.problem
        training_dir_in = os.path.join(INPUT_ROOT_DIR, 'concept_assertion_relation_training_data')
        test_labels_dir_in = os.path.join(INPUT_ROOT_DIR, "reference_standard_for_test_data")
        test_text_dir_in = os.path.join(INPUT_ROOT_DIR, "test_data")

        # target folder structure, repeated in annotations/ and in root
        # i2b2/2010/gold_{date}/
        #    train/
        #    test/
        ann_train_dir = os.path.join(OUTPUT_ANNOTATION_ROOT_DIR, "train")
        ann_test_dir = os.path.join(OUTPUT_ANNOTATION_ROOT_DIR, "test")
        text_train_dir = os.path.join(OUTPUT_TEXT_ROOT_DIR, "train")
        text_test_dir = os.path.join(OUTPUT_TEXT_ROOT_DIR, "test")

        os.makedirs(ann_train_dir, exist_ok=True)
        os.makedirs(ann_test_dir, exist_ok=True)
        os.makedirs(text_train_dir, exist_ok=True)
        os.makedirs(text_test_dir, exist_ok=True)

        # ---------------
        # Start with the training data
        # The training data is split into data from "Beth Israel" (beth) and "partners"
        ann_file_list = []
        for dataset_name in INSTITUTE_FOLDERS:
            dataset_path_in = os.path.join(training_dir_in, dataset_name, ann_type.name)

            ann_files = common.get_file_list(dataset_path_in, str(ann_type.value))
            operations_logger.info(f"Queued {len(ann_files)} files from {dataset_path_in} for conversion.")
            ann_file_list += [
                {
                    "source_file": filename,
                    "dataset": dataset_name,
                    "file_id": self.parse_file_id(filename),
                    "context": DataContext.train,
                }
                for filename in ann_files
            ]

        # ---------------
        # Iterate the test data; this is a holdout dataset and shouldn't be used until the very end of model tuning!
        # ann_type name needs to be pluralized here, because the folder names are inconsistent
        ann_type_name = ann_type.name + "s" if ann_type.name == AnnotationType.concept.name else ann_type.name
        test_dataset_path_in = os.path.join(test_labels_dir_in, ann_type_name)
        ann_files = common.get_file_list(test_dataset_path_in, str(ann_type.value))
        operations_logger.info(f"Queued {len(ann_files)} files from {test_dataset_path_in} for conversion.")
        ann_file_list += [
            {
                "source_file": filename,
                "dataset": DataContext.test,
                "file_id": self.parse_file_id(filename),
                "context": DataContext.test,
            }
            for filename in ann_files
        ]
        operations_logger.info(f"Collated {len(ann_file_list)} files for annotation conversion")

        # --------------------------
        # convert annotation files, write to output destination
        operations_logger.info(f"Writing out {len(ann_file_list)} ann/txt pairs")
        for ann_file_dict in ann_file_list:
            operations_logger.info(f"Parsing file: {ann_file_dict['source_file']}")
            file_context = ann_file_dict["context"]
            if file_context == DataContext.train:
                raw_text_base_path = os.path.join(training_dir_in, ann_file_dict["dataset"], "txt")
            elif file_context == DataContext.test:
                raw_text_base_path = test_text_dir_in
            else:
                operations_logger.error(f"Got bad DataContext for source ann file: {ann_file_dict}")
                continue

            raw_text_filepath = os.path.join(raw_text_base_path, ann_file_dict["file_id"] + ".txt")
            raw_text = common.read_text(raw_text_filepath)
            ann_text = common.read_text(ann_file_dict['source_file'])

            parsed_ann = self.parse_i2b2_label_annotation_text(
                ann_text,
                raw_text,
                target_label=target_label,
                i2b2_label=i2b2_label,
                label_filter_type_marker=LabelMarkers.type,
                label_filter_type_target=concept_type_filter,
            )
            brat_ann_doc = parsed_ann.to_file_content()

            # write annotation and text files out
            ann_file_path = os.path.join(
                OUTPUT_ANNOTATION_ROOT_DIR, ann_file_dict["context"], f"{ann_file_dict['file_id']}.ann")
            common.write_text(brat_ann_doc, ann_file_path)
            text_file_path = os.path.join(
                OUTPUT_TEXT_ROOT_DIR, ann_file_dict["context"], f"{ann_file_dict['file_id']}.txt")
            common.write_text(raw_text, text_file_path)

        # write out manifest so we know where each file came from
        file_manifest = {"manifest": ann_file_list}
        manifest_file_name = os.path.join(OUTPUT_ANNOTATION_ROOT_DIR, "manifest.json")
        common.write_json(file_manifest, manifest_file_name)

        operations_logger.info(f"Finished writing dataset to {OUTPUT_ANNOTATION_ROOT_DIR} and {OUTPUT_TEXT_ROOT_DIR}")

    @staticmethod
    def parse_file_id(filename: str) -> str:
        """
         '/opt/S3/I2B2/2010 Relation Challenge/concept_assertion_relation_training_data/beth/concept/record-28.con'
         -> 'record-28'
        """
        return os.path.splitext(os.path.split(filename)[1])[0]


if __name__ == "__main__":
    start_time = time.time()
    # create the diagnosis dataset
    i2b2_2010_reader = I2B22010ProblemReader()
    problem_label = ProblemLabel.diagnosis.name
    i2b2_2010_reader.convert_label_annotation_to_brat(target_label=problem_label, i2b2_label=LabelMarkers.concept)

    operations_logger.info(f"Extraction took {time.time()-start_time:0.1f} s")
