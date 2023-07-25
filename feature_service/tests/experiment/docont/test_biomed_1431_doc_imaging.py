import unittest
from feature_service.tests.experiment.docont import loinc_tools

README = "http://build.fhir.org/ig/HL7/ccda-on-fhir/ValueSet-2.16.840.1.113883.11.20.9.59.html"

dicom_sections_strict = """
121181|DICOM Object Catalog
121060|History
121062|Request
121064|Current Procedure Descriptions
121066|Prior Procedure Descriptions
121068|Previous Findings
121070|Findings (DIR)
121072|Impressions
121074|Recommendations
121076|Conclusions
121078|Addendum
121109|Indications for Procedure
121110|Patient Presentation
121113|Complications
121111|Summary
121180|Key Images
"""

dicom_sections_relax = """
121064|Current Procedure
121066|Prior Procedure
121070|Findings
121109|Procedure Indications 
121110|Patient Presentation
121113|Complications
121111|Summary
121180|Images
"""

loinc_sections_strict = """
#11329-0|HISTORY GENERAL
#55115-0|REQUESTED IMAGING STUDIES INFORMATION
#55111-9|CURRENT IMAGING PROCEDURE DESCRIPTIONS
55114-3|PRIOR IMAGING PROCEDURE DESCRIPTIONS
18834-2|RADIOLOGY COMPARISON STUDY - OBSERVATION
18782-3|RADIOLOGY STUDY OBSERVATION
19005-8|RADIOLOGY - IMPRESSION
18783-1|RADIOLOGY STUDY - RECOMMENDATION
55110-1|CONCLUSIONS
55107-7|ADDENDUM
18785-6|RADIOLOGY REASON FOR STUDY
55108-5|CLINICAL PRESENTATION
55109-3|COMPLICATIONS
55112-7|DOCUMENT SUMMARY
55113-5|KEY IMAGES
"""

loinc_sections_relax = """
11329-0|HISTORY
55115-0|REQUESTED IMAGING
55111-9|CURRENT IMAGING
55114-3|PRIOR IMAGING
18834-2|COMPARISON STUDY
18782-3|STUDY OBSERVATION
19005-8|IMPRESSION
18783-1|STUDY RECOMMENDATION
18785-6|REASON FOR STUDY
55108-5|CLINICAL PRESENTATION
55109-3|COMPLICATIONS
55112-7|DOCUMENT SUMMARY
55113-5|KEY IMAGES
"""

class TestBiomed1431_DoctType_Imaging(unittest.TestCase):

    def test(self):
        actual  = None # TODO

        missing = loinc_tools.list_missing_headers(actual)

        self.assertEqual(0, len(missing), f"{missing}")
