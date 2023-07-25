from text2phenotype.constants.features.feature_type import FeatureType
from feature_service.features.hint import MatchHint
from feature_service.features.feature import Feature


class Status(MatchHint):
    feature_type = FeatureType.status

    BEGINNING = ['ordered', 'begun', 'prescribed', 'began', 'started']
    IN_PROGRESS = ['pending', 'in progress', 'progress', 'continued', 'continuing']
    ENDING = ['end', 'completed', 'terminated', 'stopped', 'ended', 'complete']

    DEFINITIONS = {
        'BEGINNING': BEGINNING,
        'IN_PROGRESS': IN_PROGRESS,
        'ENDING': ENDING
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)
