###############################################################################################
# -- TEXT2HEALTH-- #
TEXT2HEALTH_SEMGROUP = {
    # https://metamap.nlm.nih.gov/Docs/SemGroups_2013.txt
    'T047': 'DiseaseDisorder',  # Disease or Syndrome
    'T195': 'Antibiotic',
    'T109': 'Medication',  # Organic Chemical
    'T184': 'SignSymptom',  # Sign or Symptom
    'T061': 'Procedure',  # Therapeutic or Preventive Procedure
    'T034': 'Lab',  # Laboratory or Test Result
    'T059': 'Lab',  # Laboratory Procedure
    # 'T060': 'Lab',  # Diagnostic Procedure
    'T060': 'Procedure',  # Diagnostic Procedure
    'T116': 'Lab',  # Amino Acid, Peptide, or Protein
}

TEXT2HEALTH_FILTERS = {
    "Diagnosis": ['MTHICD9', 'ICD9CM', 'ICD10CM', 'SNOMEDCT_US'],
    "DiseaseDisorder": ['MTHICD9', 'ICD9CM', 'ICD10CM', 'SNOMEDCT_US'],
    "Medication": ['RXNORM'],
    "Procedure": ['CPT'],
    "Lab": ['LNC', 'CPT']
}
###############################################################################################
# -- BLACKLIST -- #

_sections = [
    'C0275723',  # oid (object identifier)
    'C0012634',  # Disease
    'C0011900',  # Diagnosis
    'C0039082',  # Syndrome
    'C1509143',  # Physical assessment findings
    'C0489531',  # History of allergies
    'C0455458',  # past medical history
    'C3841837',  # Hospitalization
    'C0239966',  # Hospital patient (finding)
    'C3840745',  # Hospital emergency department
    'C0559546',  # Adverse Reactions
    'C1628992',  # Admission Diagnosis
    'C1627937',  # Medications on Admission
    'C0042196',  # Vaccination
]
_social = [
    'C0035253',  # Smoking
    'C1519384',  # Smoking History
    'C0337671',  # Former smoker
    'C0040336',  # Tobacco use disorder
    'C1519384',  # Smoking History
    'C1968515',  # Pack (physical object)
    'C0301611',  # Liquor
    'C0002638',  # Liquor
    'C1522704',  # Excercise Pain Management
    'C0015259',  # Excercise
    'C0026606',  # Physical activity
    'C0035253',  # Rest
    'C0225326',  # Fiber (Diet & Fitness)
]
_family = [
    'C0332123',  # no family history of
    'C0424909',  # Family history with explicit context pertaining to father
    'C0241889',  # Family history with explicit context
    'C0557086',  # No relatives (No family)
    'C0425043',  # death of relative
    'C0080103',  # relation
    'C0869014',  # relation
]
_measure = [
    'C1305866',  # Weighing patient
    'C0204658',  # Measuring height of patient
    'C0442735',  # Nothing
]
_other_ignore = [
    'C0262926',  # history of
    'C0421451',  # DOB
    'C0007465',  # Cause of death
    'C1546956',  # Death
    'C3668988',  # Alert status
    'C1527075',  # Revised
    'C2349001',  # Human Study Subject
]

_wrong = [
    'C0009186',  # valley fever
]

_allergy = [
    'C0014806',  # Erythromycin (not as medication)
    'C0487782',  # Ambien
    'C0700940',  # CARDIZEM
    'C1241098',  # CARDIZEM
    'C0020740',  # IBUPROFEN
]

_hepc = [
    'C0006826',  # "CA" is California not cancer
    'C0037125',  # Silver
    'C1514241',  # Positive
    'C1514241',  # Positive Finding
    'C0007457',  # Caucasoid Race
    'C0043157',  # Caucasians
    'C0032854',  # Poor
    'C1261327',  # Family history: Asthma
]

TEXT2HEALTH_BLACKLIST_CUI = set(_sections + _social + _family + _allergy + _measure + _family + _other_ignore + _hepc)

#####################################################################################
# TODO: JASON: we should have these filters and human readable map referenced here.

# not sure about that earlier comment above^^^
# as of 12/2/17, I think this SANDS info does not belong in text2phenotype-py at all
# it probably belong in the sands configuration (we might want to build this into the UI
# and make it user configurable, which would be hard if it lives here in text2phenotype-py)
# -JB
SANDS_FILTERS = {
    "DiseaseDisorder": ["MTH", "NCI", "ICD9CM", "SNOMEDCT_US", "CHV", "MDR"],
    "Medication": ["MTH", "NCI", "RXNORM", "NDFRT"],
    "Procedure": ["MTH", "NCI", "ICD9CM", "SNOMEDCT_US", "CPT"],
    "Lab": ["MTH", "CPT", "CHV", "LNC", "SNOMEDCT_US", "ABBREV"]
}

SANDS_HUMAN_READABLE_MAP = [
    ("DiseaseDisorder", "Problem List and Conditions"),
    ("Procedure", "Procedures"),
    ("Medication", "Medication"),
    ("Lab", "Lab Tests"),
    ("AnatomicalSite", "Anatomical Site")
]
