from collections import defaultdict
import re
from typing import List

from text2phenotype.constants.features import FeatureType

from feature_service.features.feature import Feature


class RegExBase(Feature):
    """Base for annotating by reg ex."""
    re_flags = re.MULTILINE | re.IGNORECASE
    extra_feature_count = 0
    rules = {}

    def annotate(self, text: str, **kwargs):
        """
        :param text: Input text
        :return: List[ (span, List[dict]) ]
        """
        # dict having entry['REGEX_NAME']=PATTERN
        regex_rules = self.rules
        matches = defaultdict(list)
        for label in regex_rules:
            pattern = regex_rules[label]
            # RegEx patterns already have a '$' token in the samples REGEX_FILE
            for match in re.finditer(pattern, text, flags=self.re_flags):
                matches[(match.start(), match.end())].append({label: text[match.start():match.end()]})

        return matches.items()

    def vectorize_token(self, token, **kwargs) -> List[int]:
        vector = self.default_vector.copy()

        self._process_hits(token, vector, self.feature_dict(sorted(self.rules.keys())))

        return vector

    def _process_hits(self, hits, feature, regex_dict):
        for hit in hits:
            self._process_hit(hit, feature, regex_dict)

    def _process_hit(self, hit, feature, regex_dict):
        regex_name = list(hit.keys())[0]
        if regex_name in regex_dict:
            feature[regex_dict[regex_name]] = 1


class DateRegEx(RegExBase):
    rules = Feature.Feature_Cache.regex_date_rules()
    extra_feature_count = 1
    feature_type = FeatureType.regex_dates
    vector_length = len(rules) + extra_feature_count

    def _process_hits(self, hits, feature, regex_dict):
        super()._process_hits(hits, feature, regex_dict)

        # last one true for all dates
        feature[-1] = 1


class AllergyRegex(RegExBase):
    feature_type = FeatureType.allergy_regex
    re_flags = re.IGNORECASE
    rules = {'$ALLERG': r'\Wallerg', '$NKDA': r'n(o)?[\W]?k(nown)?[\W]?(d(rug)?)?[\W]?a(llerg)?'}
    vector_length = len(rules)


class FindingRegex(RegExBase):
    feature_type = FeatureType.finding_regex
    rules = Feature.Feature_Cache.regex_finding_rules()
    vector_length = len(rules)


class MeasurementRegex(RegExBase):
    feature_type = FeatureType.measurement
    re_flags = re.IGNORECASE
    rules = {
        '$GREATER': r'(greater than)|>|(at least)',
        '$LESS': r'(less than)|<',
        '$DIGITS': r'((\s*x\s*)?\d(\.\d)?)+'
    }
    vector_length = len(rules)




# OTHER REGEX GROUPS
AGE = {'$AGEGENDER1', '$AGEGENDER2', '$WRITTEN_AGE_10_100_DIV10', '$WRITTEN_AGE_110_TO_119', '$WRITTEN_AGE_20_TO_99',
       '$WRITTEN_AGE_1_TO_19', '$AGE_word', '$YEARS_word', '$AGE6', '$AGE8'}
GENDER = {'$AGEGENDER1', '$AGEGENDER2', '$GENDER1', '$GENDER2', '$GENDER3'}
DOCTOR = {'$SURGEON1', '$SURGEON2', '$SURGEON3', '$SURGEON4', '$SURGEON5', '$SURGEON6', '$SURGEON7',
          '$SURGEON8', '$ASST', '$ASST2', '$ASST3', '$PA', '$RN', '$nurse', '$DR', '$MD', '$TECH', '$DOCTOR',
          '$DOCTOR0_1', '$DOCTOR0_2', '$DOCTOR0', '$DOCTOR1', '$DOCTOR2', '$DOCTOR3',
          '$DOCTOR4', '$DOCTOR_OLDER', '$DOCTOR_GEN', '$DOCTOR_SUBHEAD'}
ADDRESS = {'$ADDRESS1', '$ADDRESS2', '$ADDRESS4', '$ADDRESS5', '$ADDRESS7', '$ADDRESS6',
           '$POBOX'}
HOSPITAL = {'$LOCATION_FLOOR_1', '$LOCTION_FLOOR_2', 'HOSPITAL_1', 'HOSPITAL_2'}
URL = {'$URL1', '$URL2', '$URL3', '$URL4'}
