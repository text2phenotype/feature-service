import unittest
from feature_service.tests.experiment.docont.grammar import *
from feature_service.tests.experiment.docont import loinc_sections

class TestBiomed1431_Grammar(unittest.TestCase):

    def test_annot(self):
        expected = {'head': 'DIAGNOSIS', 'match':'relax'}
        actual  = annot('match', 'relax', 'DIAGNOSIS')
        self.assertEqual(expected, actual)

    def test_head(self):
        expect = 'DISCHARGE SUMMARY'
        actual = head('DISCHARGE SUMMARY')

        self.assertEqual(expect, actual.get('head'))

    def test_demographics_suggest(self):
        for loinc, entries in loinc_sections.make_demographics().items():
            for header in entries:
                if loinc not in ['42078-6', '76437-3']:
                    self.assertEqual('patient', header.get('who'), f"{header}")
                    self.assertEqual('demographics', header.get('visit'), f"{header}")

    def test_discharge(self):

        expected = ['DISCHARGE DIAGNOSIS', 'DISCHARGE MEDICATIONS']

        actual = [When.discharge(Match.relax(header)) for header in expected]
        actual = [entry['head'] for entry in actual]

        self.assertEqual(set(expected), set(actual))

    def test_patient_name(self):
        expected = [{'head': 'FIRST NAME', 'who': 'patient'}, {'head': 'LAST NAME', 'who': 'patient'}]

        patient_name = ['FIRST NAME', 'LAST NAME']

        actual1 = [Who.patient(header) for header in patient_name]
        actual2 = list(map(Who.patient, patient_name))
        actual3 = apply(Who.patient, patient_name)

        self.assertEqual(expected, actual1)
        self.assertEqual(expected, actual2)
        self.assertEqual(expected, actual3)


    def test_procedure(self):
        expect = {'head':'PACEMAKER', 'procedure':'device'}
        actual = Procedure.device('PACEMAKER')
        self.assertEqual(expect, actual)

        expect['rank'] = 'high'
        actual = Rank.high(Procedure.device('PACEMAKER'))
        self.assertEqual(expect, actual)

        expect = ['VENTILLATOR', 'PACEMAKER']
        actual = Rank.high(Flag.common(expect))

        print(actual)

