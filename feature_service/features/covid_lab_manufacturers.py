from feature_service.features.feature import Feature
from feature_service.features.regex import RegExBase
from text2phenotype.constants.features import FeatureType


class CovidLabManufacturers(RegExBase):
    feature_type = FeatureType.covid_lab_manufacturer
    rules = Feature.Feature_Cache.regex_covid_manufacturers()
    extra_feature_count = 1
    vector_length = len(rules) + extra_feature_count
