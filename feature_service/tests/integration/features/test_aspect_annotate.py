import unittest

from feature_service.features import Aspect, AspectEnforce, AspectLine


class AspectAnnotateTests(unittest.TestCase):

    TEST_INPUT = """Mr. Carolyn V. Blose External ID:530-79-5301 DOB:1932-07-29 Sex:Female 2017-07-19: Admitting
                 diagnoses: Bloody diarrhea Shortness of breath congestive heart failure Discharge diagnosis: 
                 Diverticulitis Valvular insufficiency Congestive Heart Failure"""

    def test_aspect_annotate(self):
        target = Aspect()
        actual = list(target.annotate(self.TEST_INPUT))

        self.assertEqual(len(actual), 3)
        self.assertEqual(actual[2], ((120, 283), ['diagnosis']))

    def test_aspect_enforce_annotate(self):
        target = AspectEnforce()
        actual = list(target.annotate(self.TEST_INPUT))

        self.assertEqual(len(actual), 3)
        self.assertListEqual(actual, [((0, 93), ['encounter']), ((93, 119), ['diagnosis']), ((120, 283), ['diagnosis'])])

    def test_aspect_line(self):
        target = AspectLine()
        actual = list(target.annotate(self.TEST_INPUT))

        self.assertEqual(len(actual), 5)
        self.assertEqual(actual[1], ((33, 92), ['demographics']))