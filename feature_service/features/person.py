from collections import defaultdict
import re

import nltk

from text2phenotype.constants.features import FeatureType

from feature_service.features.feature import Feature


class Person(Feature):
    feature_type = FeatureType.person
    vector_length = 1

    def annotate(self, text: str, **kwargs):
        """
        Match input text against a known list of PERSON_NAMES
        """
        person_names = kwargs.get('person_names', self.Feature_Cache.person_names())
        min_char_length = kwargs.get('min_char_length', 3)

        matches = defaultdict(list)

        # TODO: this is a hack to speed up very slow performance
        tokens = nltk.word_tokenize(text)
        tokens = [t.lower() for t in tokens]

        for candidate in set(tokens).intersection(set(person_names)):

            if len(candidate) < min_char_length:
                continue

            # pattern must use word boundary
            pattern = (r'\b%s\b' % candidate)

            # person names are Uppercase
            for match in re.finditer(pattern, text.lower(), flags=re.MULTILINE):

                index = (match.start(), match.end())
                token = text[match.start():match.end()]

                matches[index].append(token)

        return matches.items()

    def vectorize_token(self, token: dict, **kwargs):
        return [1]
