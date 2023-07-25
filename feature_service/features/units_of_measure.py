from collections import defaultdict

from text2phenotype.constants.features.feature_type import FeatureType
from feature_service.features.feature import Feature
from feature_service.constants.unit_bin import UnitBin
import re


class UnitsOfMeasure(Feature):
    feature_type = FeatureType.units_of_measure
    vector_length = 8

    def annotate(self, text: str, **kwargs):
        units = self.Feature_Cache.units_of_measure_resource()
        matches = defaultdict(list)

        # lower text with gaps to simplify regex pattern. e.g corner case when unit is a last word in the text
        lower_case_text = ' ' + text.lower() + ' '
        for unit in units:
            for match in re.finditer(f'[\b\s]({unit})[\b\s:;,]', lower_case_text):
                range_key = (match.start(1)-1, match.end(1)-1)
                matches[range_key].append(unit)
        return matches.items()

    def vectorize_token(self, token: list, **kwargs):
        vector = self.default_vector.copy()
        vector[0] = 1
        for unit in token:
            vector[1] = max(vector[1], UnitBin.contains_slash.check(unit))
            vector[2] = max(vector[2], UnitBin.contains_percent.check(unit))
            vector[3] = max(vector[3], UnitBin.contains_mg.check(unit))
            vector[4] = max(vector[4], UnitBin.contains_mol.check(unit))
            vector[5] = max(vector[5], UnitBin.contains_day.check(unit))
            vector[6] = max(vector[6], UnitBin.contains_time.check(unit))
            vector[7] = max(vector[7], UnitBin.contains_weight.check(unit))

        return vector
