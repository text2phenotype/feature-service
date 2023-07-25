from datetime import datetime
import os
import time
from typing import List, Dict, Any

from sklearn.model_selection import train_test_split

from text2phenotype.common import common
from text2phenotype.common import aws
from text2phenotype.common.log import operations_logger
from feature_service.feature_service_env import FeatureServiceEnv
from text2phenotype.constants.features.label_types import MedLabel
from text2phenotype.annotations.i2b2_reader import I2B2Reader, DataContext


# input folder constants
I2B2_2009_DIR = os.path.join("I2B2", "2009 Medication Challenge")
INPUT_ROOT_DIR = os.path.join(FeatureServiceEnv.DATA_ROOT.value, I2B2_2009_DIR)
TRAIN_TEST_DIR = os.path.join(INPUT_ROOT_DIR, "train.test.released.8.17.09")
TRAIN_DIR = os.path.join(INPUT_ROOT_DIR, "training.sets.released")
ANNOTATION_DIR = os.path.join(INPUT_ROOT_DIR, "annotations_ground_truth", "converted.noduplicates.sorted")

# output folder constants
cur_date = datetime.now().strftime('%Y%m%d')
RELATIVE_OUTPUT_DIR = os.path.join(I2B2_2009_DIR, f"gold_{cur_date}")
SPLIT_TEXT_OUTPUT_DIR = os.path.join(FeatureServiceEnv.DATA_ROOT.value, RELATIVE_OUTPUT_DIR, "raw_text")
SPLIT_ANNOTATION_OUTPUT_DIR = os.path.join(
    FeatureServiceEnv.DATA_ROOT.value, "annotations", RELATIVE_OUTPUT_DIR, "raw_text")
FULL_TEXT_OUTPUT_DIR = os.path.join(FeatureServiceEnv.DATA_ROOT.value, RELATIVE_OUTPUT_DIR, "full_test_set")
FULL_ANNOTATION_OUTPUT_DIR = os.path.join(
    FeatureServiceEnv.DATA_ROOT.value, "annotations", RELATIVE_OUTPUT_DIR, "full_test_set")

BUCKET_NAME = "biomed-data"
I2B2_EXPERT_LABEL_S3 = "shannon.fee/I2B2/2009 Medication Challenge/gold/gold_raw_text"
I2B2_FULL_TEST_ANN = "annotations/I2B2/2009 Medication Challenge/gold_20210215/full_test_set"

# used to strip from ends of text
STOP_PUNCTUATION = ",.:;?!"

# use this for consistent train/test split
SPLIT_RANDOM_SEED = 1234567890


class MedLabelMarkers:
    """
    Markers used in 2009 Medication dataset
    1. medication name and its offset (marker "m")
    2. dosage and its offset (marker "do")
    3. mode/route of administration and its offset
    4. frequency and its offset (marker "f")
    5. duration and its offset (marker "du")
    6. reason and its offset (marker "r")
    7. event (marker "e")
    8. temporal marker (marker "t")
    9. certainty (marker "c")
    10. found in list/narrative of the text (marker "ln")
    """

    medication = "m"
    dosage = "do"
    mode = "mo"
    frequency = "f"
    duration = "du"
    reason = "r"
    event = "e"
    temporal = "t"
    certainty = "c"
    list_narrative = "ln"


def convert_drug_annotation_to_brat():
    """
    Main method for converting I2B2 2009 Medication labels and text to .txt and brat .ann files

    The "train" files do not have any annotated data that match them;
    presumably these files are to be used for unsupervised pretraining

    We split the "test" files into "train" and "test"

    1) Identify list of train and test files; the train_test folder has duplicates of the train
    2) Copy text files to the correct data context: train and test. Train can be further separated to train/dev later
    3) Iterate through I2B2 annotation files, write to BRAT format
    4) Create file manifest for which annotation files link to which DataContext
    """
    os.makedirs(SPLIT_TEXT_OUTPUT_DIR, exist_ok=True)
    os.makedirs(SPLIT_ANNOTATION_OUTPUT_DIR, exist_ok=True)
    os.makedirs(FULL_TEXT_OUTPUT_DIR, exist_ok=True)
    os.makedirs(FULL_ANNOTATION_OUTPUT_DIR, exist_ok=True)

    train_subfolders = [
        os.path.join(TRAIN_DIR, folder)
        for folder in os.listdir(TRAIN_DIR)
        if os.path.isdir(os.path.join(TRAIN_DIR, folder))
    ]
    # train files are listed across numerical subfolders, eg "7/{file_id}"
    train_files = {
        name: os.path.join(subfolder, name)
        for subfolder in train_subfolders
        for name in os.listdir(subfolder)
        if os.path.isfile(os.path.join(subfolder, name))
    }
    train_ids = set(list(train_files.keys()))

    train_test_files = {
        name: os.path.join(TRAIN_TEST_DIR, name)
        for name in os.listdir(TRAIN_TEST_DIR)
        if os.path.isfile(os.path.join(TRAIN_TEST_DIR, name))
    }
    train_test_ids = set(list(train_test_files.keys()))
    train_intersect = train_ids.intersection(train_test_ids)
    assert (
        train_intersect == train_ids
    ), "Found incomplete match between the train_test and train intersection"
    test_ids = train_test_ids - train_ids
    test_files = {name: train_test_files[name] for name in test_ids}

    # create the split dataset folders, get annotation files
    os.makedirs(os.path.join(SPLIT_ANNOTATION_OUTPUT_DIR, DataContext.train), exist_ok=True)
    os.makedirs(os.path.join(SPLIT_ANNOTATION_OUTPUT_DIR, DataContext.test), exist_ok=True)
    ann_file_list = common.get_file_list(ANNOTATION_DIR, "m")
    ann_file_map = {get_file_id_from_ann_path(ann_file): ann_file for ann_file in ann_file_list}
    ann_file_ids = list(ann_file_map.keys())

    train_ann_files, test_ann_files = train_test_split(ann_file_ids, test_size=0.2, random_state=SPLIT_RANDOM_SEED)

    # iterate through the annotation files
    i2b2_reader = I2B2Reader()
    target_label = MedLabel.get_category_label().persistent_label
    i2b2_label = MedLabelMarkers.medication  # select the annotation we are focusing on

    ann_file_context_list = []  # which files are associated with which context
    for file_id, ann_file in ann_file_map.items():
        operations_logger.info(f"Parsing file: {ann_file}")
        if file_id in train_ann_files:
            file_context = DataContext.train
        elif file_id in test_ann_files:
            file_context = DataContext.test
        else:
            file_context = DataContext.na
        operations_logger.info(f"File {ann_file} in context '{file_context}'")
        raw_text = common.read_text(train_test_files[file_id])
        ann_text = common.read_text(ann_file)

        # get the AnnotationSet from the i2b2 annotation
        # note that internally we specify which annotation labels we keep
        # TODO: specify annotations externally from the parser, eg med/reason/dose
        parsed_ann = i2b2_reader.parse_i2b2_label_annotation_text(ann_text, raw_text, target_label=target_label, i2b2_label=i2b2_label)
        brat_ann_doc = parsed_ann.to_file_content()

        # write annotation files out
        split_ann_file_path = os.path.join(SPLIT_ANNOTATION_OUTPUT_DIR, file_context, f"{file_id}.ann")
        common.write_text(brat_ann_doc, split_ann_file_path)
        # update the file manifest with the file context
        ann_file_context_list.append({file_id: file_context})

        full_ann_file_path = os.path.join(FULL_ANNOTATION_OUTPUT_DIR, f"{file_id}.ann")
        common.write_text(brat_ann_doc, full_ann_file_path)


    operations_logger.info(f"Created {len(ann_file_map)} new BRAT annotation files")

    # create a manifest that contains the list of which annotation file points to which data context
    context_map_path = os.path.join(SPLIT_ANNOTATION_OUTPUT_DIR, "manifest.json")
    ann_data_context_map = {"annotation_file_data_context": ann_file_context_list}
    common.write_json(ann_data_context_map, context_map_path)

    # copy the existing files to the output folders
    i2b2_reader.copy_raw_text_context(list(train_files.values()), SPLIT_TEXT_OUTPUT_DIR, DataContext.pretrain)
    # split the test files into train/test/na

    train_files_out = [file_path for file_id, file_path in test_files.items() if file_id in train_ann_files]
    test_files_out = [file_path for file_id, file_path in test_files.items() if file_id in test_ann_files]
    na_files_out = [
        file_path
        for file_id, file_path in test_files.items()
        if file_id not in test_ann_files and file_id not in train_ann_files
    ]
    # copy text files to matching folder
    i2b2_reader.copy_raw_text_context(train_files_out, SPLIT_TEXT_OUTPUT_DIR, DataContext.train)
    i2b2_reader.copy_raw_text_context(test_files_out, SPLIT_TEXT_OUTPUT_DIR, DataContext.test)
    i2b2_reader.copy_raw_text_context(na_files_out, SPLIT_TEXT_OUTPUT_DIR, DataContext.na)


def intersection_from_s3_prefixes(prefix_one, prefix_two, bucket_name=BUCKET_NAME):
    """
    Given two S3 prefixes in the same bucket, parse them for the file_id and return the intersection
    """
    file_keys_one = list(aws.get_matching_s3_keys(bucket_name, prefix=prefix_one, suffix=".ann"))
    # if path has an extra dir between the root and the filename, drop it
    file_keys_one = [file_key for file_key in file_keys_one if os.path.split(file_key)[0] == prefix_one]
    file_ids_one = [get_file_id_from_ann_path(file_key) for file_key in file_keys_one]

    file_keys_two = list(aws.get_matching_s3_keys(bucket_name, prefix=prefix_two, suffix=".ann"))
    file_keys_two = [file_key for file_key in file_keys_two if os.path.split(file_key)[0] == prefix_two]
    file_ids_two = [get_file_id_from_ann_path(file_key) for file_key in file_keys_two]
    key_intersect = set(file_ids_one).intersection(set(file_ids_two))
    return key_intersect


def get_file_id_from_ann_path(ann_file):
    """
    Assumes that we have an absolute path, the filename is the last element, and the filename starts with the id
    :example:
        >>> get_file_id_from_ann_path("/my/data/root/21234.Guergana.Savova.Mayo.Clinic.m")
        "21234"
    """
    file_id = os.path.split(ann_file)[1].split(".")[0]
    return file_id


if __name__ == "__main__":

    start_time = time.time()
    convert_drug_annotation_to_brat()
    operations_logger.info(f"Extraction took {time.time()-start_time:0.1f} s")
