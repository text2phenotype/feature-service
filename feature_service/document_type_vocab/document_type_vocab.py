import os
import pickle
from typing import List

import joblib
import numpy as np

from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier

from feature_service.resources import DOCUMENT_TYPE_VOCAB_MODEL
from text2phenotype.common import common
from text2phenotype.common.log import operations_logger
from text2phenotype.constants.common import FileExtensions
from text2phenotype.constants.features import DocumentTypeLabel

from feature_service.feature_set.feature_cache import FeatureCache
from feature_service import RESULTS_PATH


class DocumentTypeVocab:
    def __init__(self, model_file_name: str = None, job_id: str = None, data_source=None):

        if not model_file_name:
            model_file_name = DOCUMENT_TYPE_VOCAB_MODEL
        self.model_file_name = model_file_name
        self.job_id = job_id
        self.cache = FeatureCache()
        self.data_source = data_source

    def predict(self, text: str) -> dict:
        """
        predict the document type of the input text
        :param text:
        :return:
        """
        prediction_matrix = self.cache.document_vectorizer().fit_transform([text])
        label_prob = self.cache.document_classifier_vocab_model(self.model_file_name).predict_proba(prediction_matrix)
        index = np.argmax(label_prob)
        proba = label_prob[0][index]
        return {'doc_type': list(DocumentTypeLabel.__members__.values())[index],
                'score': proba}

    def train(self):
        """
        train a word based neural nets for document classifier
        """
        file_list = self.data_source.get_original_raw_text_files()
        training_matrix, training_labels, vectorizer = self.__label_documents(file_list, True)
        operations_logger.info('training model...')
        # read in bsv file and create training examples and labels
        operations_logger.debug("Feature Matrix size is %s" % str(training_matrix.shape))

        training_labels = np.array(training_labels)

        # model was initialized and then updated through the training phase
        model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(300,), random_state=1)
        operations_logger.info('start training document classifier')
        model.fit(training_matrix, training_labels)
        operations_logger.info('finish training document classifier')

        return model, vectorizer.vocabulary_

    def test(self):
        """
        test the vocab based neuro net document model
        """
        file_list = self.data_source.get_original_raw_text_files()
        testing_matrix, testing_labels, _ = self.__label_documents(file_list)
        predicted_labels = self.cache.document_classifier_vocab_model(self.model_file_name).predict(testing_matrix)
        # TODO: return confusion matrix too and misclassfication report
        report_file_name = f'report_{os.path.split(self.model_file_name)[1]}.txt'
        report_file_path = os.path.join(RESULTS_PATH, self.job_id,  report_file_name)
        common.write_text(str(classification_report(testing_labels, predicted_labels)), report_file_path)

    def __label_documents(self, file_paths: List[str], train: bool = False):
        """
        label the document type for each document
        :param file_paths: a list of file paths
        :return:
        """
        testing_text = []
        testing_labels = []
        document_type_label_feature = DocumentTypeLabel()
        for file_path in file_paths:
            text = common.read_text(file_path)
            # get the label
            option_list = file_path.split('/')
            if 'txt' in option_list:
                txt_index = option_list.index(FileExtensions.TXT.value)
                doc_type_parsed = option_list[txt_index + 1]
                doc_type_enum = DocumentTypeLabel.from_brat(doc_type_parsed)
            else:
                doc_type_enum = DocumentTypeLabel.pathology
            # pathology is in a different file structure in
            testing_text.append(text)
            testing_labels.append(
                document_type_label_feature.vectorize([], doc_type=doc_type_enum, token_based=False))
        vectorizer = self.cache.document_vectorizer(train, self.model_file_name)
        testing_matrix = vectorizer.fit_transform(testing_text)
        testing_labels = np.array(testing_labels)
        return testing_matrix, testing_labels, vectorizer

    def save(self, model, **kwargs):
        """
        save the model and vocabulary
        :return:
        """
        model_file_name = self.model_file_name
        operations_logger.debug(f'Saving model: {model_file_name}')
        model_file_path = os.path.join(RESULTS_PATH, self.job_id, model_file_name)
        if not os.path.exists(os.path.dirname(model_file_path)):
            os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
        pickle.dump(model, open(model_file_path, 'wb'))
        vocabulary = kwargs.get('vocabulary')
        if vocabulary:
            operations_logger.debug(f'Saving vocabulary File')
            vocab_file_path = os.path.join(RESULTS_PATH, self.job_id, f'{model_file_name}_vocabulary.sav')
            joblib.dump(vocabulary, vocab_file_path)
        return model_file_path
