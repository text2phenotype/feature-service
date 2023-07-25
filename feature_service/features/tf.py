from abc import ABC

from text2phenotype.constants.features import FeatureType

from feature_service.features.feature import Feature


class TFBinary(Feature, ABC):
    annotated_feature = 'token'
    requires_annotation = False
    uppercase = True
    vector_length = 1
    _corpus = {}

    def vectorize_token(self, token, **kwargs):
        if self.uppercase:
            search = token.upper()
        else:
            search = token
        if search in self._corpus:
            return [1]


class TF(TFBinary, ABC):
    num_bins = 11
    idf_weight = 1
    vector_length = 11
    uppercase = False

    def __init__(self):
        super().__init__()
        self.default_vector[0] = 1

    def vectorize_token(self, token: str, **kwargs):
        if self.uppercase:
            search = token.upper()
        else:
            search = token
        if search in self._corpus:
            vector = self.zero_vector.copy()
            token_tf = self._corpus[search]
            for j in range(1, self.num_bins):
                if token_tf < self.idf_weight * j:
                    vector[j] = 1
                    break
            return vector


class I2B2(TF):
    feature_type = FeatureType.tf_i2b2
    _corpus = Feature.Feature_Cache.tf_i2b2()
    idf_weight = 84


class CCDA(TF):
    feature_type = FeatureType.tf_ccda
    _corpus = Feature.Feature_Cache.tf_ccda()
    idf_weight = 300


class MTSample(TF):
    feature_type = FeatureType.tf_mtsample
    _corpus = Feature.Feature_Cache.tf_mtsamples()
    idf_weight = 99


class MRConSo(TF):
    feature_type = FeatureType.tf_mrconso
    _corpus = Feature.Feature_Cache.tf_mrconso()
    idf_weight = 10500


class NPICity(TFBinary):
    feature_type = FeatureType.tf_npi_city
    _corpus = Feature.Feature_Cache.tf_npi_city()


class NPIAddress(TFBinary):
    feature_type = FeatureType.tf_npi_address
    _corpus = Feature.Feature_Cache.tf_npi_address()


class NPIPhone(TFBinary):
    feature_type = FeatureType.tf_npi_phone
    _corpus = Feature.Feature_Cache.tf_npi_phone()


class PatientFirstName(TFBinary):
    feature_type = FeatureType.tf_patient_first_name
    _corpus = Feature.Feature_Cache.tf_patients_first_name()


class PatientLastName(TFBinary):
    feature_type = FeatureType.tf_patient_last_name
    _corpus = Feature.Feature_Cache.tf_patients_last_name()


class NPIFirstName(TFBinary):
    feature_type = FeatureType.tf_npi_first_name
    _corpus = Feature.Feature_Cache.tf_npi_first_name()


class NPILastName(TFBinary):
    feature_type = FeatureType.tf_npi_last_name
    _corpus = Feature.Feature_Cache.tf_npi_last_name()


class Cities(TFBinary):
    feature_type = FeatureType.tf_cities
    _corpus = Feature.Feature_Cache.tf_usa_cities()


class States(TFBinary):
    feature_type = FeatureType.tf_states
    _corpus = Feature.Feature_Cache.tf_usa_states()


class Disorder(TFBinary):
    feature_type = FeatureType.tf_disorder

    _corpus = Feature.Feature_Cache.tf_snomed_vocab_disorder()


class Finding(TFBinary):
    feature_type = FeatureType.tf_finding
    _corpus = Feature.Feature_Cache.tf_snomed_vocab_finding()


class Procedure(TFBinary):
    feature_type = FeatureType.tf_procedure
    _corpus = Feature.Feature_Cache.tf_snomed_vocab_procedure()
