from text2phenotype.constants.features import FeatureType

from feature_service.features.feature import Feature
from feature_service.features.hint import MatchHint


class VitalSigns(MatchHint):
    feature_type = FeatureType.vital_signs
    
    # Temperature
    celcius = r'(?:celcius|°c|°|c)'
    farenheit = r'(?:farenheit|°f|°|f|(deg f))'

    TEMP_FEVER_F = rf'10[0-6](?:\.[0-9])? ?{farenheit}'
    TEMP_NORMAL_F = rf'9[7-9](?:\.[0-9])? ?{farenheit}'
    TEMP_FEVER_C = rf'(?:3[89]|4[01])(?:\.[0-9])? ?{celcius}'
    TEMP_NORMAL_C = rf'(?:36(?:\.[0-9])?|37(?:\.[12])?) ?{celcius}'

    #no matches for temp_c from 37.3 to 37.9

    DEGREES = rf'celcius|°c|°f|c|farenheit|°|f'

    temperature = f'(?P<TEMP_FEVER_C>{TEMP_FEVER_C})' \
                  f'|(?P<TEMP_FEVER_F>{TEMP_FEVER_F})' \
                  f'|(?P<TEMP_NORMAL_C>{TEMP_NORMAL_C})' \
                  f'|(?P<TEMP_NORMAL_F>{TEMP_NORMAL_F})'

    # Breaths
    BREATHS_UNIT = r'breaths/min|respirations|RR|respiratory rate|resp'
    breaths_template = rf'(?P<breath_unit>(?:{BREATHS_UNIT}) ?)?{{}}(?(breath_unit)| ?({BREATHS_UNIT}))'
    BREATHS_MINUTE_NORMAL = r'1[2-8]'  # 12-18
    BREATHS_MINUTE_LOW = r'1[01]'  # 10-11
    BREATHS_MINUTE_HIGH = r'(?:19|[2-6][0-9])'  # 19-69

    # BPM
    bpm_unit = r'(?:beats per minute|bpm)'
    bpm_template = rf'{{}}(?: ?{bpm_unit})'

    bpm_resting_normal = bpm_template.format(r'(?:[6-9][0-9]|100)')

    BPM_20_70 = r'(?:[789][0-9]|1[0-7][0-9])' #70-179

    bpm_header = rf'pulse(\s{1,3}rate)?'
    temp_header = 'temp(erature)?'

    # Oxygen
    OXYGEN_CONTENT = r'O2 ?CT|oxygen content|[O0]2 content'
    OXYGEN_SATURATION = r'(?:oxygen saturation|O2 saturation|SpO2|O2 ?SAT|Oxygen sat)'
    oxygen_template = rf'(?P<oxy_sat_unit>(?:{OXYGEN_SATURATION}) ?)?{{}}(?(oxy_sat_unit)| ?({OXYGEN_SATURATION}))'
    OXYGEN_SATURATION_NORMAL = r'(?:9[5-9]|100)(?:\.[0-9][0-9]?)?'  #95.00-100.99

    # BMI
    bmi_unit = r'BMI|Body Mass Index|Body Mass'
    height = r'height|Ht'
    weight = r'weight|Wt'
    
    BMI = rf'(?P<bmi_unit>{bmi_unit})'\
          rf'|(?P<height>{height})'\
          rf'|(?P<weight>{weight})'

    # Mental status
    phq2 = r'PHQ[- ]?2'
    phq9 = r'PHQ[- ]?9'
    screen= r'screen(?:ing(?: for)?)?'
    MENTAL_STATUS = rf'(?:(?:{phq2})|(?:{phq9}))(?: ?{screen})?'

    DEFINITIONS = {
        'TEMPERATURE': [temperature],
        'DEGREES': [celcius, farenheit],
        'BMI': [BMI],
        'MENTAL_STATUS': [MENTAL_STATUS],
        'BREATHS_UNIT': [BREATHS_UNIT],
        'BREATHS_MINUTE_NORMAL': [rf'(?P<BREATHS_MINUTE_NORMAL>{BREATHS_MINUTE_NORMAL})'],
        'BREATHS_MINUTE_LOW': [rf'(?P<BREATHS_MINUTE_LOW>{BREATHS_MINUTE_LOW})'],
        'BREATHS_MINUTE_HIGH': [rf'(?P<BREATHS_MINUTE_HIGH>{BREATHS_MINUTE_HIGH})'],
        'BPM_20_70': [BPM_20_70],
        'BPM_UNIT': [bpm_unit],
        'BPM_HEADER': [bpm_header],
        'TEMP_HEADER': [temp_header],
        'OXYGEN_CONTENT': [OXYGEN_CONTENT, OXYGEN_SATURATION],
        'OXYGEN_SATURATION_NORMAL': [rf'(?P<OXYGEN_SATURATION_NORMAL>{OXYGEN_SATURATION_NORMAL})'],
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)