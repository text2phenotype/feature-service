from text2phenotype.constants.features import FeatureType
from feature_service.features.feature import Feature
from feature_service.features.hint import MatchHint


class PathologyReport(MatchHint):
    """
    https://www.cancer.gov/about-cancer/diagnosis-staging/diagnosis/pathology-reports-fact-sheet
    """
    feature_type = FeatureType.pathology_report

    # healthcare setting
    PATHOLOGY = ['cancer center', 'cancer pathology', 'pathology department', 'department of pathology']
    ONCOLOGY = ['oncology attending note', 'oncologist note', 'oncology note', 'oncologist']
    SURGICAL = ['surgical pathology']

    # Pathology Report
    TITLE = ['pathology report', 'path report', 'pathologic findings']
    GROSS = ['gross description', 'macroscopic']
    MICROSCOPIC = ['microscopic']
    TISSUE = ['tissue specification', 'tissue site', 'anatomic site']
    BIOPSY = ['biopsy', 'biopsies']
    SPECIMEN = ['specimen type', 'specimen size', 'specimen', 'specimens', 'pathology case']
    TUMOR = ['tumor site', 'tumor size', 'tumor extent', 'tumor location', 'histologic type']
    LYMPH = ['sentinel lymph node', 'lymph nodes', 'lymph node']

    # Pathology Keywords affecting severity
    MARGINS = ['margins', 'margin']
    RESECTION = ['resection', 'resected']
    UNRESECTABLE = ['unresectable']

    # Type of tumor/cancer and grade (how abnormal the cells look under the microscope and how
    # quickly the tumor is likely to grow and spread)
    DIAGNOSIS = ['pathology diagnosis', 'pathologic diagnosis', 'final diagnosis text']
    SNOMED = ['snomed codes', 'snomed', 'snomed-ct', 'snomedct', 'snomed ct']

    GRADE = ['histologic grade', 'tumor grade', 'cancer grade', 'nottingham', 'ajcc']
    STAGE = ['pathological staging', 'pathologic stage', 'staging']
    TNM = ['tnm staging', 'tnm classification', 'tnm stage', 'pathologic tnm']

    FISH = ['FISH', 'Fluorescence', 'Fluorescent', 'in-situ hybridization', 'hybridization']
    FFPE = ['formalin', 'paraffin']
    H_AND_E = ['h&e', 'hematoxylin', 'eosin']
    GENES = ['genetics', 'genetic', 'genes', 'gene', 'mutation', 'exon', 'intron']

    ################################################################################################################

    DEFINITIONS = {

        # Healthcare Settting
        'PATHOLOGY': PATHOLOGY,
        'SURGICAL': SURGICAL,
        'ONCOLOGY': ONCOLOGY,

        # Pathology Report
        'TITLE': TITLE,
        'GROSS': GROSS,
        'TISSUE': TISSUE,
        'BIOPSY': BIOPSY,
        'SPECIMEN': SPECIMEN,
        'TUMOR': TUMOR,
        'MARGINS': MARGINS,
        'RESECTION': RESECTION,
        'UNRESECTABLE': UNRESECTABLE,
        'LYMPH': LYMPH,
        'MICROSCOPIC': MICROSCOPIC,
        'DIAGNOSIS': DIAGNOSIS,
        'SNOMED': SNOMED,
        'GRADE': GRADE,
        'STAGE': STAGE,
        'TNM': TNM,

        # Hint FISH and H&E and GENS so model leans to filter out
        'FISH': FISH,
        'FFPE': FFPE,
        'H_AND_E': H_AND_E,
        'GENES': GENES
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))

    vector_length = len(CONST_KEYS)
