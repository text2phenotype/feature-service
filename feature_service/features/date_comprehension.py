from collections import defaultdict

from text2phenotype.common.dates import parse_dates
from text2phenotype.constants.features import FeatureType

from feature_service.features.feature import Feature


class DateComprehension(Feature):
    feature_type = FeatureType.date_comprehension
    vector_length = 3

    since_first = 'first'
    before_last = 'last'

    def annotate(self, text: str, **kwargs):
        dates = parse_dates(text)
        dates.sort()

        matches = defaultdict(list)
        if dates:
            first_date = dates[0][0]
            last_date = dates[-1][0]
            for date in dates:
                span = date[1]

                matches[span].append({self.since_first: (date[0] - first_date).days <= 1,
                                      self.before_last: (last_date - date[0]).days <= 1,
                                      'day': date[0].day,
                                      'month': date[0].month,
                                      'year': date[0].year
                                      })
            return matches.items()

    def vectorize_token(self, token: dict, **kwargs):
        # date parsed
        # earliest date
        # latest date
        vector = self.default_vector.copy()
        vector[0] = 1
        if token[0][self.since_first] == True:
            vector[1] = 1
        if token[0][self.before_last] == True:
            vector[2] = 1

        return vector
