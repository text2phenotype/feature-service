import unittest

from feature_service.tests.experiment.docont import loinc_tools

class TestBiomed1431_DoctType_LabCorp(unittest.TestCase):

    def test(self):
        actual  = ['LabCorp',
                    'LabCorp Patient Report',
                    'Enzo Clinical Labs',
                    'TOPA Diagnostics',
                    'Quest Diagnostics',
                    'Quest',
                    'CVS', 'CVS/Pharmacy',
                    'CareMark', 'CVS|CareMark',
                    # 'LABORATORY REPORT',
                    # 'Lab Report',
                    'Physician Details',
                    'ACCESSION #',
                    'Specimen Details',
                    'Specimen ID',
                    'DOB',
                    'AGE',
                    'Gender',
                    'PHone',
                    'Patient ID',
                    'Date Collected',
                    'Date Received',
                    'Date Entered',
                    'Date Reported',
                    # 'Ordering',
                    # 'Referring',
                    'NPI',
                    # 'Ordered Items',
                    'TESTS',
                    # 'RESULT',
                    'FLAG',
                    # 'UNITS',
                    # 'INTERVAL'
                    'REFERENCE',
                    'FINAL REPORT',
                    'DATE ISSUED',
                    'SPECIMEN INFORMATION']

        missing = loinc_tools.list_missing_headers(actual)

        self.assertEqual(0, len(missing), f"{missing}")




