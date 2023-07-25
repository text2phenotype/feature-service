
from feature_service.features import Person
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase


class PersonAnnotateTests(AnnotateTestsBase):

    def test_person_annotate(self):

        target = Person()

        actual = target.annotate(self.TEST_INPUT_CAROLYN)

        self.assertTrue(self.find_match('Carolyn', actual))
        self.assertTrue(self.find_match('Blose', actual))

