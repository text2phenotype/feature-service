import unittest
from feature_service.features.covid_lab_manufacturers import CovidLabManufacturers

class  TestsCovidManufacturers(unittest.TestCase):
    TXT = " BioCerna SARS_COV 2  Bio-Rad Laboratories, Inc  Atila BioSystem"

    def test_annotation(self):
        feat = CovidLabManufacturers()
        annot = feat.annotate(self.TXT)
        self.assertEqual(len(annot), 3)

        expected = [
            ((22, 37), [{'$LABORATORY_MANUFACTURURER': 'Bio-Rad Laborat'}]),
            ((1, 9), [{'$MANUFACTURER_ONE_WORD': 'BioCerna'}]),
            ((49, 58), [{'$MANUFACTURER_BIOTECH': 'Atila Bio'}])]

        self.assertListEqual(list(annot), expected)
