###############################################################################
#
# EXPERT HINTS
#
###############################################################################
ENCOUNTER = [
    'PCP', 'primary care physician', 'primary care doctor',
    'hospitalization'
    'hospital', 'medical center',
    'clinic',
    'appointment',
    'consult', 'consults', 'consultation',
    'episode', 'episodes',
    'recommendation',
    'admit', 'admitted', 'admission',
    'evaluation',
    'discharge', 'discharged',
    'ER', 'emergency room', 'emergency department',
    'OR', 'operating room',
    'procedure',
    'surgical', 'surgery',
    'transplant', 'transplant center', 'transplantation center',
    'pediatric', 'adult'
                 'operating room',
    'ICU', 'intensive care unit',
    'CT', 'CT scan', 'CT-scan',
    'pathology',
    'dermatology',
    'endocrine'
]

LATERALITY = [
    'lateral',
    'bilaterally',
    'proximal',
    'distal',
    'horizontal', 'horizontally',
    'front', 'anterior', 'head?',
    'back', 'posterior', 'dorsal', 'rear', 'tail?',
    'left', 'sinister', 'left-hand', 'left hand',
    'right', 'dexter', 'right-hand', 'right hand',
    'center', 'medial', 'middle',
    'lower',
    'upper',
    'cranial'
]

SUBJECTIVE = [
    'symptoms', 'signs',
    'appear', 'appears', 'appear normal', 'appears normal', 'appearance',
    'color', 'colors', 'coloration',
    'suggests', 'suggestive',
    'around',
    'clear',
    'good',
    'hope', 'hopes',
    'literally',
    'extensive',
    'abnormal', 'abnormality',
    'inspection',
    'stable',
    'future',
    'denies', 'deny',
    'scale',
]
OBJECTIVE = [
    'definite',
    'evidence',
    'size',
    'cm',  # centimeters
    'pressure', 'mmHg',
    'estimated',
    'elevated', 'elevation',
    'flow',
    'rate',
    'descending', 'ascending',
    'gross', 'grossly',
]

LUNGS = [
    'SOB',  # Shortness of Breath
]

KIDNEY = [
    'CKD',
    'GFR',  # glomerular filtration rate
]

NEURO = [
    'TIA',  # transient ischemic attack (stroke)
    'CVA',  # cardiovascular accident (stroke)
]

HEART = [
    'JVD',  # jugular vein distention
    'ECG', 'echocardiogram',
    'S1', 'S2', 'S3', 'S4',  # sounds of heart, 1st,2nd,3rd,4th
    'LV'  # Left Ventricle
    'MI',  # Myocardial Infarction, Heart attack
    'DVT',  # Deep Vein Thrombosis
    'PE',  # Pulmonary Embolism
    'PMI',  # Point of Maximal Impulse
    'ST',  # EKG measure of heart
    'ST-T',  # EKG measure of heart,
    'VTE',  # Benous ThromboEmbolism
    'cardiac',
    'veins',
    'pulmonary',
    'systolic', 'systolic function'
                'ventricular',
    'artery', 'atrium', 'atrial', 'aortic',
    'calcified',
]

###############################################################################
#
# EXPERT HINTS
#
###############################################################################

SKIN = ['skin']

COMBO = ['and', 'with', 'and/or', 'between']

FANBOY = ['for', 'and', 'nor', 'but', 'or', 'yet', 'between']

STAGE = [
    'stage III',
]

GRADE = [  # TODO: very incomplete
    'grade 2', 'grade 2/6',
    'grade 4', 'grade IV'
]

PRONOUN = ['he', 'she', 'they', 'them', 'man', 'woman', 'adult', 'male', 'woman', 'child']
TEMPORAL = ['prior', 'before', 'after', 'last', 'recent', 'recently', 'morning', 'afternoon', 'night', 'tonight']

PROSTATE = [
    'BPH',  # benign prostatic hyperplasia
]
