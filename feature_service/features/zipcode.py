from collections import defaultdict
import re

import nltk

from text2phenotype.constants.features import FeatureType

from feature_service.features.feature import Feature


class ZipCode(Feature):
    feature_type = FeatureType.zipcode
    vector_length = 1

    def annotate(self, text: str, **kwargs):
        min_char_length = kwargs.get('min_char_length', 5)
        zip_dict = self.Feature_Cache.zip_codes_dict()
        zip_codes = set(self.Feature_Cache.zip_codes_list())

        matches = defaultdict(list)
        for match in re.finditer(r'\b\d{5}(-\d{4})?\b', text, flags=re.MULTILINE):
            index = (match.start(), match.end())
            zip5 = match.group(0)[:5]

            if len(zip5) < min_char_length or zip5 not in zip_codes:
                continue

            matches[index].append(zip_dict.get(zip5))

        return matches.items()

    def vectorize_token(self, token, **kwargs):
        vector = self.default_vector.copy()
        vector[0] = 1
        return vector
