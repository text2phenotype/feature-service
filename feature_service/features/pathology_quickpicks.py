from text2phenotype.constants.features import FeatureType
from feature_service.features.feature import Feature
from feature_service.features.hint import MatchHint


class PathologyQuickPicks(MatchHint):
    """"
    Quick Picks by Pathologists for Pathologists
    https://www.dfhcc.harvard.edu/research/core-facilities/pathology-specimen-locator/

    Clinical expert definitions for pathology reports in "simplest pathology terms"
    https://github.com/text2phenotype/text2phenotype-samples/blob/dev/shrine/cancer_quick_picks.json
    """
    feature_type = FeatureType.pathology_quickpicks

    LEUKEMIA = ['acute leukemia', 'aml']
    BLADDER = ['bladder carcinoma', 'transitional cell carcinoma', 'transitional cell']
    BRAIN = ['glioblastoma', 'astrocytoma', 'glioma', 'medulloblastoma']
    BREAST = ['breast adenocarcinoma', 'breast carcinoma', 'DCIS']
    CERVICAL = ['cervix carcinoma', 'cervical carcinoma', 'cervix  adenocarcinoma', 'cervical adenocarcinoma']
    COLON = ['colon carcinoma', 'colonic carcinoma', 'rectum carcinoma', 'rectal carcinoma', 'colon adenocarcinoma',
             'colonic adenocarcinoma', 'rectum adenocarcinoma', 'rectal adenocarcinoma']
    ESOPHAGUS = ['esophageal carcinoma', 'esophagus carcinoma', 'esophageal adenocarcinoma', 'esophagus adenocarcinoma']
    KIDNEY = ['kidney carcinoma', 'renal carcinoma', 'kidney adenocarcinoma', 'renal adenocarcinoma']
    LIVER = ['hepatoma', 'hepatocellular carcinoma', 'hepatocellular', 'HCC']
    LUNG = ['lung carcinoma', 'lung adenocarcinoma', 'NSCLC']
    LYMPHOMA = ['non hodgkin lymphoma', 'non-hodgkin', 'non hodgkin', 'lymphoma', 'NHL']
    MESOTHELIOMA = ['mesothelioma']
    OVARY = ['ovary carcinoma', 'ovarian carcinoma', 'fallopian tube carcinoma', 'ovary adenocarcinoma',
             'ovarian adenocarcinoma', 'fallopian tube adenocarcinoma']
    PANCREAS = ['pancreatic carcinoma', 'pancreas carcinoma', 'pancreatic adenocarcinoma', 'pancreas adenocarcinoma']
    SARCOMA = ['sarcoma', 'angiosarcoma', 'osteosarcoma', 'chondrosarcoma', 'fibrosarcoma', 'rhabdomyosarcoma',
               'leiomyosarcoma']
    SKIN = ['melanoma', 'skin carcinoma', 'skin adenocarcinoma']
    STOMACH = ['gastric carcinoma', 'stomach carcinoma', 'gastric adenocarcinoma', 'stomach adenocarcinoma']
    THYROID = ['thyroid carcinoma', 'thyroid adenocarcinoma']
    UTERUS = ['uterine carcinoma', 'uterus carcinoma', 'endometrium carcinoma', 'endometrial carcinoma',
              'uterine adenocarcinoma', 'uterus adenocarcinoma', 'endometrium adenocarcinoma',
              'endometrial adenocarcinoma']

    DEFINITIONS = {
        'LEUKEMIA': LEUKEMIA,
        'BLADDER': BLADDER,
        'BRAIN': BRAIN,
        'BREAST': BREAST,
        'CERVICAL': CERVICAL,
        'COLON': COLON,
        'ESOPHAGUS': ESOPHAGUS,
        'KIDNEY': KIDNEY,
        'LIVER': LIVER,
        'LUNG': LUNG,
        'LYMPHOMA': LYMPHOMA,
        'MESOTHELIOMA': MESOTHELIOMA,
        'OVARY': OVARY,
        'PANCREAS': PANCREAS,
        'SARCOMA': SARCOMA,
        'SKIN': SKIN,
        'STOMACH': STOMACH,
        'THYROID': THYROID,
        'UTERUS': UTERUS
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))

    vector_length = len(CONST_KEYS)
