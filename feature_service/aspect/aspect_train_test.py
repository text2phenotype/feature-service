import os
from typing import List, Tuple
from datetime import datetime

import numpy as np
import joblib
from sklearn.metrics import classification_report, confusion_matrix

from text2phenotype.common.log import operations_logger
from text2phenotype.common import aspect_samples
from text2phenotype.common import common
from text2phenotype.ccda.section import Aspect as AspectEnum
from text2phenotype.constants.environment import Environment
from feature_service import RESULTS_PATH
from feature_service.constants import AspectModelType
from feature_service.feature_set.feature_cache import FeatureCache
from feature_service.resources import ASPECT_CLASSIFIER_MODEL
from feature_service.feature_service_env import FeatureServiceEnv


# expected source for training data
# pull this resource with:
# $ aws s3 cp s3://biomed-data/aspect /opt/S3/aspect --recursive
TRAINING_DATA_PATH = os.path.join(
    os.environ["MDL_BIOM_DATA_ROOT"],
    "aspect/training-examples")


def load_aspect_bsv_dataset(bsv_filepath: str) -> Tuple[List[str], List[int]]:
    """
    Read in the target `aspect` model dataset
    Expecting line format like:
        Aspect.value|text -- for example '4|aspirin twice daily'

    """
    raw_text = common.read_text(bsv_filepath)
    text_samples = []
    label_samples = []
    for line in raw_text.split("\n"):
        # remove the 'None.' token and blank string for training data.
        line_list = line.split('|')
        if len(line_list) < 2:
            if len(line_list) == 1 and line_list[0] == "":
                continue
            else:
                # print(f"malformed line: {line_list}")
                continue
        text = line_list[1].strip()
        label = line_list[0]
        if text == 'None.' or not text:
            continue
        else:
            label_samples.append(int(label))
            text_samples.append(text)

    return text_samples, label_samples


def train_model_from_bsv(file_bsv, model_name_suffix, job_id, model_type: AspectModelType = AspectModelType.nn):
    """
    Train model from many examples.
    :param file_bsv: Aspect.value|text -- for example '4|aspirin twice daily'
    :param model_name_suffix: str, suffix name for the model output file
    :param job_id: str
    :param model_type: AspectModelType, enum for the model type, defaults to a sklearn neural net
        expected to be an instantiated & empty sklearn estimator object in the value
    :return: path to classifier, based on job_iud and model_name_suffix
    """
    # load the data
    training_text, training_labels = load_aspect_bsv_dataset(file_bsv)

    operations_logger.info('Starting model training...')

    # initialize vectorizer with the current tokenizer
    vectorizer = FeatureCache().aspect_vectorizer()
    model = model_type.value  # be more explicit about the model class object
    # set model to be verbose
    model.verbose = True

    # vectorize the training text
    training_features = vectorizer.fit_transform(training_text)

    operations_logger.debug("Feature Matrix size is %s" % str(training_features.shape))

    training_labels = np.array(training_labels)

    # model was initialized and then updated through the training phase
    operations_logger.info('start training aspect labeler')
    model.fit(training_features, training_labels)
    operations_logger.info('finish training aspect labeler')

    # silence the model before we save it
    model.verbose = False

    # what if we overwrite the old model file with new one because we are using the same name.
    # save the model file to a binary file
    model_name = f"aspect_{model_type.name}_{model_name_suffix}"

    operations_logger.info(f"Model name: {model_name}")

    out_path = os.path.join(RESULTS_PATH, job_id)
    os.makedirs(out_path, exist_ok=True)
    model_path = os.path.join(out_path, f"{model_name}_model.joblib")
    joblib.dump(model, model_path)
    # save the vocabulary
    joblib.dump(vectorizer.vocabulary_, os.path.join(out_path, f"{model_name}_vocabulary.joblib"))

    train_mean_accuracy = model.score(training_features, training_labels)
    operations_logger.debug(f"Training mean accuracy = {train_mean_accuracy}")

    return model_path


# set a default classifier
def test_model_from_bsv(file_bsv, job_id, model_file_path=None, use_target_names=True):
    """
    Test model against many examples.

    :param file_bsv: test file
    :param job_id: name for the job train/test job run
        Writes reports to feature-service/results/{job_id}/
    :param model_file_path: the name of the model to be tested, e.g., nn or nn_mt_i2b2_ccda
        expects full path?
    :return: None
    prints accuracy, precision-recall f1 score, confusion_matrix
    """
    operations_logger.info('Starting model test...')

    test_text, test_labels = load_aspect_bsv_dataset(file_bsv)
    dataset_name = os.path.basename(file_bsv)

    operations_logger.info('loading pre-trained model')
    model = FeatureCache().aspect_classifier(model_file_path)
    # the aspect classifier uses the default model name if not specified
    model_name = os.path.splitext(os.path.basename(model_file_path or ASPECT_CLASSIFIER_MODEL))[0]
    vectorizer = FeatureCache().aspect_vectorizer()

    test_features = vectorizer.transform(test_text)
    test_labels = np.array(test_labels)

    mean_accuracy = model.score(test_features, test_labels)
    operations_logger.info(f"Test mean accuracy is: {mean_accuracy:.3f}")

    predicted_labels = model.predict(test_features)

    target_names = [f"{a.name} ({a.value})" for a in AspectEnum.get_active_aspects()] if use_target_names else None
    report = classification_report(test_labels, predicted_labels, target_names=target_names, digits=3)
    print(report)
    cm = confusion_matrix(test_labels, predicted_labels)
    print(cm)

    # write out the reports
    os.makedirs(os.path.join(RESULTS_PATH, job_id), exist_ok=True)
    report_file_name = f"report_{model_name}_{dataset_name}.txt"
    report_file_path = os.path.join(RESULTS_PATH, job_id, report_file_name)
    common.write_text(report, report_file_path)
    cm_file_path = os.path.join(RESULTS_PATH, job_id, f"confusion_matrix_{model_name}_{dataset_name}.txt")
    common.write_text(str(cm), cm_file_path)

    operations_logger.info("Finished Testing")


if __name__ == "__main__":
    """
    NOTES (mjp) 2021.03.17:
    The origin dataset for the aspect model `nn_med_no_header_model.sav` is rather unclear.
    There are many bsv files with the parsed aspect labels, buried in a version of `text2phenotype-samples` f316ba98
    under the folder text2phenotype-samples/training-examples/
    These files originally came from the GDrive, where they were expected to be in biomed/aspect/{train|test}
    
    We have more data these days, so in theory we can recreate this model dataset, and dramatically 
    improve the quality of the aspect model
    """
    # switch for whether or not we want to run a trained model on all known datasets
    TEST_ALL_DATASETS = False

    # given dataset, train and evaluate new aspect model
    TRAIN_NEW_MODEL = False
    TEST_NEW_MODEL = True

    # given dataset, evaluate the dataset on the released model
    TEST_ORIG_MODEL = False

    # concatenated_all.bsv contains 12 classes over 30k+ samples
    # train_filename = "concatenated_all.bsv"
    train_filename = "all_combined.bsv"  # does better than concatenated_all;
    train_dataset_name = os.path.splitext(train_filename)[0]

    job_id = f"aspect_train_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    model_path = None

    train_model_suffix = f"{train_dataset_name}_{datetime.now().strftime('%Y%m%d')}"

    bsv_filename = os.path.join(TRAINING_DATA_PATH, train_filename)
    if TRAIN_NEW_MODEL:
        model_path = train_model_from_bsv(bsv_filename, train_model_suffix, job_id, model_type=AspectModelType.nn)

    if TEST_NEW_MODEL:
        if not model_path:
            fixed_path = "aspect_train_20210607_134724/aspect_nn_med_no_header_20210607_model.joblib"
            model_path = os.path.join(RESULTS_PATH, fixed_path)
        test_model_from_bsv(bsv_filename, job_id=job_id, model_file_path=model_path)

    if TEST_ORIG_MODEL:
        # will not work with sklearn>=0.24.1
        test_model_from_bsv(bsv_filename, job_id=job_id, model_file_path=model_path)

    if TEST_ALL_DATASETS:
        train_datasets = common.get_file_list(TRAINING_DATA_PATH, ".bsv")
        for bsv_filename in train_datasets:
            print(f"Test on file: {bsv_filename}")
            # train_filename = os.path.join(TRAINING_DATA_PATH, bsv_filename)
            try:
                test_model_from_bsv(bsv_filename, job_id=job_id, model_file_path=model_path)
            except Exception as e:
                operations_logger.error(f"Error in dataset: {e.args[0]}")
                continue

    operations_logger.info(f"Finished job_id: {job_id}")
