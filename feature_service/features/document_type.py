import os

import fasttext

from feature_service.features.feature import Feature, FeatureType
from feature_service.feature_service_env import FeatureServiceEnv

from text2phenotype.common import common
from text2phenotype.constants.features.label_types import DocumentTypeLabel
from text2phenotype.doc_type.predict import get_doc_types


class DocumentType(Feature):
    feature_type: FeatureType = FeatureType.document_type
    vector_length: int = len(DocumentTypeLabel) - 1

    def __init__(self):
        super().__init__()
        self.__classifier = None
        self.__stop_words = None

    def annotate(self, text: str, **kwargs):
        if not self.__classifier:
            self.__load_classifier()

        result = []
        for prediction in get_doc_types(text, self.__classifier, self.__stop_words):
            result.append((prediction['range'], [prediction['label']]))

        return result

    def vectorize_token(self, token, **kwargs):
        vector = self.default_vector.copy()

        vector[DocumentTypeLabel.get_from_persistent_label(token[0]).value.column_index - 1] = 1

        return vector

    def __load_classifier(self):
        resource_dir = os.path.join(FeatureServiceEnv.MODELS_PATH.value, 'resources', 'files', 'doc_type')
        self.__classifier = fasttext.load_model(os.path.join(resource_dir, 'fasttext_label_8020_20210201.bin'))
        self.__stop_words = eval(common.read_text(os.path.join(resource_dir, 'stopwords.txt')))
