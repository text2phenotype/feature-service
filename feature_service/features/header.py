from collections import defaultdict
import re

from text2phenotype.constants.features import FeatureType

from feature_service.feature_set.feature_cache import FeatureCache
from feature_service.features.feature import Feature


class Header(Feature):
    feature_type = FeatureType.header
    vector_length = 1

    def annotate(self, text: str, **kwargs):
        """
        :return: Dictionary: (replace_token) => (index[(start, end)])
        """
        # TODO: refactor to use featureset.hint
        min_char_length = kwargs.get('min_char_length', 3)
        matches = defaultdict(list)
        aspect_map = FeatureCache().aspect_map()
        for header in aspect_map.keys():
            if len(header) < min_char_length:
                continue
            # pattern must use word boundary
            pattern_upper = (r'\b%s\b' % header)
            # headers are Uppercase
            for match in re.finditer(pattern_upper, text, flags=re.MULTILINE):
                index = (match.start(), match.end())
                matches[index].append({header: aspect_map[header]})
        return matches.items()

    def vectorize_token(self, token: dict, **kwargs):
        return [1]
