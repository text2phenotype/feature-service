from functools import partial

from . import guess

def head(header_obj)->dict:
    """
    Convert (guard/ensure) header_obj is a dict type
    :param header_obj: if str return like {head='DIAGNOSIS'} return returns header_obj if dict
    :return: dictionary containing {header='DIAGNOSIS', ... + optional key=vals}
    """
    if isinstance(header_obj, str):
        return {'head': header_obj.upper()}
    elif isinstance(header_obj, dict):
        if 'head' not in header_obj.keys():
            raise Exception(f'head not found in {header_obj}')
        return header_obj
    raise Exception(f'head function did not recognize header object type {header_obj}')

def annot(key, value, header_obj):
    """
    annotate header with key=value
    :param key: 'match'
    :param value: 'relax'
    :param header_obj: 'DIAGNOSIS'
    :return: dict like {head='DIAGNOSIS' match='relax'}
    """
    if isinstance(header_obj, str):
        return {'head':header_obj.upper(), key:value}

    elif isinstance(header_obj, list):
        return [annot(key, value, head(h)) for h in header_obj]

    elif isinstance(header_obj, dict):
        if 'head' in header_obj: # Entry detected
            if key in header_obj.keys():  # Existing value
                if isinstance(value, bool):
                    if value != header_obj[key]!=value:
                        print(f'flag? key={key} value={value} header={header_obj}')
                elif header_obj[key] not in value: # Existing value does not match passed value
                    # print(f'skip! key={key} value={value} header={header_obj}')
                    pass
            else:
                header_obj[key] = value
            return header_obj
        else: # NOT entry YES loinc:headers mapping
            target = dict()
            for loinc, synonyms in header_obj.items():
                target[loinc] = annot(key, value, synonyms)
            return target
    else:
        raise Exception(f'unrecognized type key={key}  value={value} header_obj={header_obj}')

def apply(functor, headers):
    """
    map a function to a list of headers, allow for parallel processing
    https://www.mathworks.com/help/parallel-computing/parfor.html
    :param functor: Person.patient
    :param headers: ['FIRST NAME', 'LAST NAME']
    :return:
    """
    if isinstance(headers, str):
        return functor(head(headers))

    if isinstance(headers, list):
        return list(map(functor, headers))

    elif isinstance(headers, dict):
        if 'head' in headers: # Entry detected
            return functor(headers)
        else:
            target = dict()
            for loinc, values in headers.items():
                target[loinc] = apply(functor, values)
            return target
    else:
        raise Exception(f'unrecognized type {headers}')

def suggest(header_obj):

    if isinstance(header_obj, str):
        return suggest(head(header_obj))

    if isinstance(header_obj, list):
        return [suggest(h) for h in header_obj]

    elif isinstance(header_obj, dict):
        if 'head' not in header_obj:
            target = dict()
            for loinc, headers in header_obj.items():
                # print(f'@ LNC = {loinc}')
                target[loinc] = suggest(headers)
            return target
        else: # {head='DISCHARGE SUMMARY', keys=vals, ....}
            _head = header_obj['head']
            _who = guess.guess_who(_head)
            _where = guess.guess_where(_head)
            _when = guess.guess_when(_head)
            _style = guess.guess_style(_head)
            _impress = guess.guess_impress(_head)
            _rank = guess.guess_rank(_head)

            if _who and 'who' not in header_obj: header_obj['who'] = _who
            if _where and 'where' not in header_obj: header_obj['where'] = _where
            if _when and 'when' not in header_obj: header_obj['when'] = _when
            if _style and 'style' not in header_obj: header_obj['style'] = _style
            if _impress and 'impress' not in header_obj: header_obj['impress'] = _impress
            if _rank and 'rank' not in header_obj: header_obj['impress'] = _rank

        return header_obj
    else:
        raise Exception(f'unrecognized type {header_obj}')

#############################################################
# Visit
#
class Visit:
    """
    ACTI|Activities & Behaviors|T057|Occupational Activity
    ACTI|Activities & Behaviors|T054|Social Behavior
    """
    key = partial(annot, 'visit')
    encounter = partial(key, 'encounter')
    demographics = partial(key, 'demographics')
    social = partial(key, 'social') # Smoking, etc.

#############################################################
# Drug
#
class Drug:
    """
    CHEM|Chemicals & Drugs|T116|Amino Acid, Peptide, or Protein
    CHEM|Chemicals & Drugs|T195|Antibiotic
    CHEM|Chemicals & Drugs|T123|Biologically Active Substance
    CHEM|Chemicals & Drugs|T122|Biomedical or Dental Material
    CHEM|Chemicals & Drugs|T118|Carbohydrate
    CHEM|Chemicals & Drugs|T103|Chemical
    CHEM|Chemicals & Drugs|T200|Clinical Drug
    """
    key = partial(annot, 'drug')
    med = partial(key, 'med')
    allergy = partial(key, 'allergy')
    immunization = partial(key, 'immunization')

#############################################################
# Procedure
#
class Procedure:
    """
    PROC|Procedures|T060|Diagnostic Procedure ( "BIOPSY" )
    PROC|Procedures|T058|Health Care Activity
    PROC|Procedures|T063|Molecular Biology Research Technique (?)
    PROC|Procedures|T061|Therapeutic or Preventive Procedure
    DEVI|Devices|T203|Drug Delivery Device
    """
    key = partial(annot, 'procedure')
    procedure = partial(key, 'procedure')
    device = partial(key, 'device') # Oxygen Therapy
    operate = partial(key, 'operate') # Operate (surgical)

class Problem:
    """
    LIVB|Living Beings|T005|Virus
    """
    key = partial(annot, 'problem')
    problem = partial(key, 'problem')
    diagnosis = partial(key, 'diagnosis')
    symptom = partial(key, 'symptom')

#############################################################
# Measure
#
class Measure:
    key = partial(annot, 'measure')
    lab = partial(key, 'lab')
    finding = partial(key, 'finding')
    vital = partial(key, 'vital')  # NEW
    imaging = partial(key, 'imaging')  # NEW
    objective = partial(key, 'objective')

#############################################################
# Exam (MIDDLE)
#
class Exam:
    """
    ANAT|Anatomy|T029|Body Location or Region
    ANAT|Anatomy|T023|Body Part, Organ, or Organ Component
    ANAT|Anatomy|T022|Body System
    """
    key = partial(annot, 'exam')
    ros = partial(key, 'ros')  # Review Of Systems
    physical = partial(key, 'physical') # physical exam

#############################################################
# Who
#
class Who:
    key = partial(annot, 'who')
    family = partial(key, 'family')
    patient = partial(key, 'patient')
    provider = partial(key, 'provider')
    payer = partial(key, 'insurance')

#############################################################
# Where
#
class Where:
    key = partial(annot, 'where')
    home = partial(key, 'home')
    hosp = partial(key, 'hosp')
    clinic = partial(key, 'clinic')
    consult = partial(key, 'consult')
    emergency = partial(key, 'emergency')
    inpatient = partial(key, 'inpatient')
    outpatient = partial(key, 'outpatient')
    pathology = partial(key, 'pathology')
    surgery = partial(key, 'surgery')
    radiology = partial(key, 'radiology')
    department = partial(key, 'department')

#############################################################
# When
#
class When:
    key = partial(annot, 'when')
    history = partial(key, 'history')
    present = partial(key, 'present')
    plan = partial(key, 'plan')
    admit = partial(key, 'admit')
    discharge = partial(key, 'discharge')
    transfer = partial(key, 'transfer')

#############################################################
# Why ( TOP of document)
#
class Why:
    key = partial(annot, 'why')
    reason = partial(key, 'reason')
    complaint = partial(key, 'complaint')
    indication = partial(key, 'indication')

#############################################################
# Match
#
class Match:
    key = partial(annot, 'match')
    pref = partial(key, 'pref')    # pref string for header
    strict = partial(key, 'strict')
    relax = partial(key, 'relax')
    abbr = partial(key, 'abbr')

#############################################################
# Style
#
class Style:
    key = partial(annot, 'style')
    narrative = partial(key, 'narrative')
    subhead = partial(key, 'subhead')
    lists = partial(key, 'lists')
    choice = partial(key, 'choice')
    unique = partial(key, 'unique')
    legal = partial(key, 'legal')
    calendar = partial(key, 'calendar')
    printer = partial(key, 'printer')

#############################################################
# Rank
#
class Rank:
    key = partial(annot, 'rank')
    first = partial(key, 'first')
    second = partial(key, 'second')
    high = partial(key, 'high')
    low = partial(key, 'low')
    ignore = partial(key, 'ignore')

#############################################################
# Tag
#
class Flag:
    multi = partial(annot, 'multi', True) # 1+ contexts
    common = partial(annot, 'common', True) # >>1 contexts


#############################################################
# Interpretation (BOTTOM)
#
class Impress:
    key = partial(annot, 'impress')
    conclude = partial(key, 'conclude')
    interpret = partial(key, 'interpret')
    notable = partial(key, 'notable')

#############################################################
# Interpretation (BOTTOM)
#
class Instruct:
    key = partial(annot, 'instruct')
    cover = partial(key, 'cover')
    care = partial(key, 'care')

#############################################################
# Graph
#
class BNF:
    visit = Visit
    drug = Drug
    procedure = Procedure
    problem = Problem
    measure = Measure
    exam = Exam

    who = Who
    where = Where
    when = When
    why = Why

    impress = Impress
    instruct = Instruct

    match = Match
    style = Style
    rank = Rank


