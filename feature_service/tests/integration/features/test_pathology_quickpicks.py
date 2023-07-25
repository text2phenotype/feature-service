from feature_service.features.pathology_quickpicks import PathologyQuickPicks
from feature_service.tests.integration.features.annotate_tests import MatchHintVectorizeBase


class PathologyQuickPicksVectorizeTests(MatchHintVectorizeBase):
    def test_vectorize_no_match(self):
        self._test_vectorize_no_match(PathologyQuickPicks())

    def test_vectorize_all(self):
        self._test_vectorize_all_definitions(PathologyQuickPicks())
