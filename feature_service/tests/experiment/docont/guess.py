from feature_service.features import PersonalHistory, Family

class Guess:
    DOB = ['BIRTH', 'DOB', 'AGE']
    DATE = ['DATE'] + DOB
    PLACE = ['CITY', 'ZIP', 'ADDRESS']
    CONTACT = ['EMAIL', 'PHONE', 'FAX', 'NAME', 'CONTACT BY']
    UNIQUE = ['EXTERNAL ID', 'ADDRESS'] + DOB + CONTACT
    KEYVAL = PLACE + UNIQUE

    # Who
    PATIENT = ['PATIENT', 'PERSONAL', 'ASSESSMENT', 'PLAN'] + UNIQUE + PersonalHistory.PERSONAL_HISTORY
    FAMILY = ['FAMILY', 'FHX'] + Family.RELATIVES
    PROVIDER = ['PROVIDER', 'PCP', 'CARE TEAM', 'COMPLETED BY', 'CONSULT', 'REFERRED BY', 'SIGNED BY', 'FAX']

    # When
    HISTORY = ['HISTORY', 'HX', 'PAST', 'COMPLETED', 'RECEIVED', 'PREVIOUS', 'PRIOR',
               'ADMINISTERED', 'PERFORMED', 'RENDERED', 'DEAD', 'DEATH']
    PRESENT = ['PRESENT', 'CURRENT', 'INDICATION', 'ACTIVE']
    PLAN = ['PLAN', 'AS NEEDED', 'RECOMMEND']
    ADMIT = ['ADMIT', 'ADMISSION', 'ADMITTED']
    DISCHARGE = ['DISCHARGE']
    TRANSFER = ['TRANSFER', 'CONSULT']

    # Where
    HOSP = ['HOSPITAL'] + ADMIT + DISCHARGE + TRANSFER
    SURGERY = ['SURGERY', 'SURGICAL', 'OPERATION', 'OPERATIVE']

    # Style
    LEGAL = ['SIGNED', 'SIGNATURE', 'CONSENT', 'DISCLOSURE', 'DISCLOSED', 'ALERT', 'OVERRIDE']
    REPORT = ['REPORT', 'DOCUMENT', 'NOTE', 'TITLE', 'DESCRIPTION', 'CONSULT', 'INTERPRET']
    NARRATIVE = REPORT + ['NARRATIVE', 'PLAN', 'INFORMATION']
    LISTS = ['LIST']

def like(header, phrases):
    if isinstance(header, dict):
        header = header['head']
    if isinstance(phrases, str):
        phrases = [phrases]

    for utterance in phrases:
        if utterance.upper() in header.upper():
            return True
    return False

def guess_who(header)->str:
    if like(header, Guess.FAMILY): return 'family'
    if like(header, Guess.FAMILY): return 'provider'
    if like(header, Guess.FAMILY): return 'patient'

def guess_when(header)->str:
    if like(header, Guess.ADMIT): return 'admit'
    if like(header, Guess.DISCHARGE): return 'discharge'
    if like(header, Guess.TRANSFER): return 'transfer'
    if like(header, Guess.HISTORY): return 'history'
    if like(header, Guess.PLAN): return 'plan'
    if like(header, Guess.PRESENT): return 'present'

def guess_where(header)->str:
    if like(header, 'pathology'): return 'pathology'
    if like(header, 'emergency'): return 'emergency'
    if like(header, Guess.HOSP): return 'hosp'
    if like(header, Guess.SURGERY): return 'surgery'
    if like(header, 'department'): return 'department'

def guess_impress(header)->str:
    if like(header, 'conclu'): return 'conclude'
    if like(header, 'notable'): return 'notable'
    if like(header, 'interpret'): return 'interpret'
    if like(header, 'assess'): return 'interpret'
    if like(header, 'eval'): return 'interpret'

def guess_style(header)->str:
    if like(header, Guess.LEGAL): return 'legal'
    if like(header, Guess.NARRATIVE): return 'narrative'
    if like(header, Guess.UNIQUE): return 'unique'
    if like(header, Guess.CONTACT): return 'unique'
    if like(header, Guess.KEYVAL): return 'choice'
    if like(header, Guess.DATE): return 'calendar'
    if like(header, Guess.LISTS): return 'lists'

def guess_rank(header)->str:
    if like(header, 'principal'): return 'first'
    if like(header, 'primary'): return 'first'
    if like(header, 'second'): return 'second'
    if like(header, 'preliminary'): return 'second'
    if like(header, 'related'): return 'high'
    if like(header, Guess.FAMILY): return 'ignore'