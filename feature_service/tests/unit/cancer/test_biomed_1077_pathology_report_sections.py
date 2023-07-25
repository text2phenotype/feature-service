import unittest
from feature_service.feature_set.feature_cache import FeatureCache


class TestBiomed1077_PathologyReportHeaders(unittest.TestCase):

    PATHOLOGY_HEADERS = """        
    Pathologic Diagnosis    
    Histopathological Diagnosis
    Clinical Diagnosis
    Procurement Date
    Formatted Path Report
    SURGICAL PATHOLOGY REPORT
    Final Diagnosis
    Final Diagnosis By
    Department
    Department Of Cancer Pathology
    Department Of Pathology
    Diagnosis
    Note
    Notes
    Clinical Data
    TISSUE SUBMITTED
    Tissue Specification
    Tissue Site
    Site of Tissue
    Anatomic Site
    Gross Description    
    Macroscopic Description
    Macroscopy
    Microscopic Description
    Microscopic Examination
    Specimen
    Specimen Type 
    Specimen Size     
    Specimens
    Specimens Submitted
    Material Collected
    Material Collected On
    Material Received
    Material Received on    
    Clinical Notes
    Pathology Report
    Pathology Case
    Tumor Classification
    Tumor Site
    Tumor Size
    Tumor Extent
    Tumor Location
    Lymph Nodes
    Margins    
    Surgical Margins
    Grossly Evident lesion
    Histologic type
    Histologic grade    
    Nottingham Histologic Score
    Staging
    Pathologic Stage
    Total Nottingham Score
    Additional Pathologic findings
    Pathologic findings
    LAB NO.
    Clinical Note
    Necrosis
    Patient History
    History
    Operation 
    Operative Findings
    Intraoperative Diagnosis
    Resident
    AJCC Classification
    """

    def test_pathology_report_headers(self):
        pathology = [p.strip() for p in self.PATHOLOGY_HEADERS.splitlines()]
        pathology = list(filter(None, pathology))

        known = FeatureCache().aspect_map()

        for header in pathology:
            self.assertTrue(header.upper() in known)
