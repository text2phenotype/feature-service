import unittest

from feature_service.tests.experiment.docont import loinc_doc
from feature_service.tests.experiment.docont import loinc_tools

################################################################
headers_cover_hedis = [ # 94137-7
    'Stars and HEDIS® Measure Guidelines and Checklist',
    'HEDIS®', 'HEDIS', 'HEDIS Measure Guidelines and Checklist',
    'HEDIS Guidelines', 'HEDIS Measure', 'HEDIS Measures']

headers_cover_healthport = [
    'Healthport', 'health port', 'HealthPortConnect',
    'Electronic Delivery Service',
    'PATIENT INDEXING',
    'Ship to', 'Bill to', 'Records from',
    'Requested By',
    'PAY YOUR INVOICE ONLINE AT']

headers_cover_disability = [
    'Requested By: DISABILITY DETERMINATION', 'DISABILITY DETERMINATION',
    'SOCIAL SECURITY ADMINISTRATION',
    'Explanation of Form SSA-827',
    'Authorization to Disclose Information to the Social Security Administration',
    'OFFICE OF DISABILITY']

headers_cover_hipaa = [
    'AUTHORIZATION TO DISCLOSE INFORMATION',
    'HIPAA', 'health insurance portability and accountability act',
    'NOTICE REQUIRED BY THE PRIVACY ACT', '45 CFR', '45CFR']

headers_cover_fax = [
    'Medical Records Request',
    'ATTENTION', 'ATTENTION!',
    'FACESHEET', 'PLEASE EXPEDITE', 'URGENT MATTER',
    'MEMBER INFORMATION']

headers_cover = headers_cover_hedis + \
                headers_cover_healthport + \
                headers_cover_disability + \
                headers_cover_hipaa + headers_cover_fax

################################################################
headers_page = [
    'Authored by',
    'Collected Date Time',
    'Department',
    'Dictated By',
    'Dictated Date',
    'Enc Date',
    'Generated on'
    'Last Updated',
    'MODIFIED REPORT',
    'Nursing Unit',
    'Patient Results',
    'Printed from',
    'Requested by',
    'REVIEW ADDENDUM SECTION',
    'Transcribed Document Print',
    'Report Status:Signed',
    'Report Status',
    'Reported Date Time',
    'Transcribed By',
    'Transcribed Date',
    'WIRB', 'WESTERN IRB',
]

################################################################
document_imaging = [
    'CLINICAL HISTORY',
    'CT, abdomen and pelvis without/with IV contrast',
    'CT GUIDED LUNG NEEDLE BIOPSY',
    'CT-guided percutaneous biopsy',
    'CT HEAD W-W/O Contrast',
    'CHEST SINGLE VIEW',
    'CHEST X-ray',
    'Diagnostic X-ray'    
    'Radiology print',
    'Radiation Oncology Consultation',
]
headers_imaging = [
    'CLINICAL INFORMATION',
    'CLINICAL HISTORY',
    'COMPARISON STUDY',
    'CONTRAST',
    'FINDINGS',
    'IMPRESSION',
    'FULL RESULT'
]

################################################################
document_pathology = [
    'COPATH CYTOLOGY REPORT',
    'PATHOLOGY REPORT',
    'Department of Pathology',
    'PATHOLOGY ADDENDUM',
    'SURGICAL PATHOLOGY CONSULTATION REPORT',
    'Tamtron Print',
    'Powerpath',
    'Cytology Request'
]

headers_pathology_genes = [
    'BIOMARKER TESTING',
    'MUTATIONAL ANALYSIS',
    'Mutation Analysis Panel Report', 'Mutation Analysis',
    'MUTATION SCREENING',
    'MOLECULAR RESULTS',
    'ORDERED GENES',
    'GENE SYMBOL', 'Exons', 'Codons'
]

headers_pathology = [
    'Accession',
    'Case Number',
    'Collected',
    'Final Dx',
    'FISH tests', 'FISH test',
    'MDL tests',
    'MATERIALS TESTED',
    'Pathology Requisition Details',
    'Received',
    'Reported',
    'Slide/Block Description',
    'Specimen',
    'Specimen Date/Time',
    'Specimen Information',
    'SPECIMEN SOURCE',
    'SurgPathNo',
    'Surg Path No',
]

################################################################
headers_oncology = [ # oncology clinic note
    'Oncology History', 'ONCOLOGIC HISTORY',
    'SURGICAL ONCOLOGY CLINIC'
]

################################################################
document_operation = [
    'Op Note',
    'Op Note by',
    'REPORT OF OPERATION',
    'Surgery clinic note'
]
headers_operation = [
    'ANESTHESIA', 'ANESTHETIST', 'ANESTHETIC',
    'ATTENDING SURGEON',
    'COMPLICATIONS',
    'DATE OF PROCEDURE',
    'DATE OF OPERATION',
    'ESTIMATED BLOOD LOSS',
    'INDICATIONS FOR SURGERY',
    'OPERATIVE FINDINGS',
    'RESIDENT SURGEON',
    'SURGEON',
    'PROCEDURE IN DETAIL',
    'TITLE OF OPERATION',
    'PROCEDURE',
    'PREOPERATIVE DIAGNOSIS',
    'POSTOPERATIVE DIAGNOSIS',
    'SERVICE'
    'SPECIMENS SENT',
]

################################################################
document_progress = [
    'Progress Notes signed by',
    'Progress Notes by',
    'Progress Note by',
    'Clinic Progress Note'
]

headers_progress = [
    'subjective', 'objective', 'assessment','plan',
    'history of present illness', 'review of systems',
]

################################################################
document_history_and_physical = [
    'H&P BY'
]

headers_history_and_physical = [
    'DATE OF VISIT',
    'CHIEF COMPLAINT',
    'HISTORY OF PRESENT ILLNESS',
    'Review of Systems',
    'Physical Exam',
    'Nursing Intake',
    'Urology Review of Systems',
    'Constitutional Symptoms',
]

################################################################
document_lab = [
    'LAB OUTPATIENT'
]

class TestBiomed1431_Cyan(unittest.TestCase):

    def test(self):
        expected = loinc_tools.dict_header_loinc().keys()

        self.assertHeaders(expected, headers_cover)

    def assertHeaders(self, expected, actual):
        missing = list()

        for header in actual:
            header = header.upper()

            if not header in expected:
                missing.append(header)

        self.assertEqual(0, len(missing), f"{missing}")


