import unittest

from feature_service.features.sectionizer import Sectionizer

TEST_TEXT = """

REVIEW OF SYSTEMS

GENERAL/CONSTITUTIONAL: The patient denies fever, fatigue, weakness,
weight gain or weight loss.  
 HEAD, EYES, EARS, NOSE AND THROAT: Eyes  - The patient denies pain,
redness, loss of vision, double or blurred vision, flashing lights or spots,
dryness, the feeling that something is in the eye and denies wearing glasses.
Ears, nose, mouth and throat. The patient denies ringing in the ears, loss of
hearing, nosebleeds, loss of sense of smell, dry sinuses, sinusitis, post
nasal drip, sore tongue, bleeding gums, sores in the mouth, loss of sense of
taste, dry mouth, dentures or removable dental work, frequent sore throats,
hoarseness or constant feeling of a need to clear the throat when nothing is
there, waking up with acid or bitter fluid in the mouth or throat, food
sticking in throat when swallows or painful swallowing.  
 CARDIOVASCULAR: The patient denies chest pain, irregular heartbeats,
sudden changes in heartbeat or palpitation, shortness of breath, difficulty
breathing at night, swollen legs or feet, heart murmurs, high blood pressure,
cramps in his legs with walking, pain in his feet or toes at night or varicose
veins.  
 RESPIRATORY: The patient denies chronic dry cough, coughing up blood,
coughing up mucus, waking at night coughing or choking, repeated pneumonias,
wheezing or night sweats.  
 GASTROINTESTINAL: The patient denies decreased appetite, nausea,
vomiting, vomiting blood or coffee ground material, heartburn, regurgitation,
frequent belching, stomach pain relieved by food, yellow jaundice, diarrhea,
constipation, gas, blood in the stools, black tarry stools or hemorrhoids.  
 GENITOURINARY: The patient denies difficult urination, pain or burning
with urination, blood in the urine, cloudy or smoky urine, frequent need to
urinate, urgency, needing to urinate frequently at night, inability to hold
the urine, discharge from the penis, kidney stones, rash or ulcers, sexual
difficulties, impotence or prostate trouble, no sexually transmitted diseases.  
 MUSCULOSKELETAL: The patient denies arm, buttock, thigh or calf cramps.
No joint or muscle pain. No muscle weakness or tenderness. No joint swelling,
neck pain, back pain or major orthopedic injuries.  
 SKIN AND BREASTS: The patient denies easy bruising, skin redness, skin
rash, hives, sensitivity to sun exposure, tightness, nodules or bumps, hair
loss, color changes in the hands or feet with cold, breast lump, breast pain
or nipple discharge.  
 NEUROLOGIC: The patient denies headache, dizziness, fainting, muscle
spasm, loss of consciousness, sensitivity or pain in the hands and feet or
memory loss.  
 PSYCHIATRIC: The patient denies depression with thoughts of suicide,
voices in ?? head telling ?? to do things and has not been seen for
psychiatric counseling or treatment.  
 ENDOCRINE: The patient denies intolerance to hot or cold temperature,
flushing, fingernail changes, increased thirst, increased salt intake or
decreased sexual desire.  
 HEMATOLOGIC/LYMPHATIC: The patient denies anemia, bleeding tendency or
clotting tendency.  
 ALLERGIC/IMMUNOLOGIC: The patient denies rhinitis, asthma, skin
sensitivity, latex allergies or sensitivity."""


class TestBiomed598(unittest.TestCase):

    def test_sectionizer(self):
        expected_matches = [
            {'HEADER_UPPER': {'match': ['REVIEW OF SYSTEMS', 2, 19],
                              'section': {'aspect': 'Aspect.physical_exam',
                                          'doctype': ['procedure_note',
                                                      'ccd',
                                                      'progress_note',
                                                      'physician_discharge_summary',
                                                      'consult_note',
                                                      'history_and_physical_note',
                                                      'CCDA',
                                                      'discharge_summary'],
                                          'header': 'REVIEW OF SYSTEMS',
                                          'loinc': '10187-3',
                                          'person': 'Person.patient',
                                          'reltime': 'RelTime.present',
                                          'style': 'StyleType.narrative'}}},
            {'HEADER_COLON': ['GENERAL/CONSTITUTIONAL:', 21, 44]},
            {'HEADER_COLON': [' HEAD, EYES, EARS, NOSE AND THROAT:', 120, 155]},
            {'HEADER_COLON': {'match': [' CARDIOVASCULAR:', 856, 872],
                              'section': {'aspect': 'Aspect.physical_exam',
                                          'doctype': [None],
                                          'header': 'CARDIOVASCULAR',
                                          'loinc': ['LA18277-6', 'LP31409-3'],
                                          'person': 'Person.patient',
                                          'reltime': 'RelTime.present',
                                          'style': 'StyleType.subheading'}}},
            {'HEADER_COLON': {'match': [' RESPIRATORY:', 1168, 1181],
                              'section': {'aspect': 'Aspect.physical_exam',
                                          'doctype': [None],
                                          'header': 'RESPIRATORY',
                                          'loinc': ['LA16975-7'],
                                          'person': 'Person.patient',
                                          'reltime': 'RelTime.present',
                                          'style': 'StyleType.subheading'}}},
            {'HEADER_COLON': {'match': [' GASTROINTESTINAL:', 1344, 1362],
                              'section': {'aspect': 'Aspect.physical_exam',
                                          'doctype': [None],
                                          'header': 'GASTROINTESTINAL',
                                          'loinc': ['LP89777-4',
                                                    '54534-3',
                                                    'LA16968-2',
                                                    'MTHU031867'],
                                          'person': 'Person.patient',
                                          'reltime': 'RelTime.present',
                                          'style': 'StyleType.subheading'}}},
            {'HEADER_COLON': {'match': [' GENITOURINARY:', 1642, 1657],
                              'section': {'aspect': 'Aspect.physical_exam',
                                          'doctype': [None],
                                          'header': 'GENITOURINARY',
                                          'loinc': ['LP89778-2',
                                                    'LA16969-0',
                                                    '54535-0',
                                                    'MTHU031868'],
                                          'person': 'Person.patient',
                                          'reltime': 'RelTime.present',
                                          'style': 'StyleType.subheading'}}},
            {'HEADER_COLON': {'match': [' MUSCULOSKELETAL:', 2022, 2039],
                              'section': {'aspect': 'Aspect.physical_exam',
                                          'doctype': [None],
                                          'header': 'MUSCULOSKELETAL',
                                          'loinc': ['MTHU031870',
                                                    'LP89781-6',
                                                    'LA16972-4',
                                                    '54538-4'],
                                          'person': 'Person.patient',
                                          'reltime': 'RelTime.present',
                                          'style': 'StyleType.subheading'}}},
            {'HEADER_COLON': [' SKIN AND BREASTS:', 2226, 2244]},
            {'HEADER_COLON': {'match': [' NEUROLOGIC:', 2474, 2486],
                              'section': {'aspect': 'Aspect.physical_exam',
                                          'doctype': [None],
                                          'header': 'NEUROLOGIC',
                                          'loinc': ['LA16973-2'],
                                          'person': 'Person.patient',
                                          'reltime': 'RelTime.present',
                                          'style': 'StyleType.subheading'}}},
            {'HEADER_COLON': [' PSYCHIATRIC:', 2634, 2647]},
            {'HEADER_COLON': {'match': [' ENDOCRINE:', 2811, 2822],
                              'section': {'aspect': 'Aspect.physical_exam',
                                          'doctype': [None],
                                          'header': 'ENDOCRINE',
                                          'loinc': ['LP31396-2'],
                                          'person': 'Person.patient',
                                          'reltime': 'RelTime.present',
                                          'style': 'StyleType.subheading'}}},
            {'HEADER_COLON': [' HEMATOLOGIC/LYMPHATIC:', 2982, 3005]},
            {'HEADER_COLON': [' ALLERGIC/IMMUNOLOGIC:', 3075, 3097]},
            {'BLANKLINE': ['\n', 0, 1]},
            {'BLANKLINE': ['\n', 1, 2]},
            {'UPPER_WORD': ['REVIEW', 2, 8]},
            {'UPPER_WORD': ['OF', 9, 11]},
            {'UPPER_WORD': ['SYSTEMS', 12, 19]},
            {'NEWLINE': ['\n', 19, 20]},
            {'BLANKLINE': ['\n', 20, 21]},
            {'UPPER_WORD': ['GENERAL', 21, 28]},
            {'UPPER_WORD_COLON': ['CONSTITUTIONAL:', 29, 44]},
            {'TITLE_WORD': ['The', 45, 48]},
            {'NEWLINE': ['\n', 89, 90]},
            {'BEGIN': ['', 90, 90]},
            {'NEWLINE': ['\n', 119, 120]},
            {'BEGIN': [' ', 120, 121]},
            {'UPPER_WORD': ['HEAD', 121, 125]},
            {'UPPER_WORD': ['EYES', 127, 131]},
            {'UPPER_WORD': ['EARS', 133, 137]},
            {'UPPER_WORD': ['NOSE', 139, 143]},
            {'UPPER_WORD': ['AND', 144, 147]},
            {'UPPER_WORD_COLON': ['THROAT:', 148, 155]},
            {'TITLE_WORD': ['Eyes', 156, 160]},
            {'TITLE_WORD': ['The', 164, 167]},
            {'NEWLINE': ['\n', 188, 189]},
            {'BEGIN': ['', 189, 189]},
            {'NEWLINE': ['\n', 265, 266]},
            {'BEGIN': ['', 266, 266]},
            {'NEWLINE': ['\n', 343, 344]},
            {'TITLE_WORD': ['Ears', 344, 348]},
            {'TITLE_WORD': ['The', 374, 377]},
            {'NEWLINE': ['\n', 421, 422]},
            {'BEGIN': ['', 422, 422]},
            {'NEWLINE': ['\n', 495, 496]},
            {'BEGIN': ['', 496, 496]},
            {'NEWLINE': ['\n', 572, 573]},
            {'BEGIN': ['', 573, 573]},
            {'NEWLINE': ['\n', 648, 649]},
            {'BEGIN': ['', 649, 649]},
            {'NEWLINE': ['\n', 725, 726]},
            {'BEGIN': ['', 726, 726]},
            {'NEWLINE': ['\n', 797, 798]},
            {'BEGIN': ['', 798, 798]},
            {'NEWLINE': ['\n', 855, 856]},
            {'BEGIN': [' ', 856, 857]},
            {'UPPER_WORD_COLON': ['CARDIOVASCULAR:', 857, 872]},
            {'TITLE_WORD': ['The', 873, 876]},
            {'NEWLINE': ['\n', 925, 926]},
            {'BEGIN': ['', 926, 926]},
            {'NEWLINE': ['\n', 1001, 1002]},
            {'BEGIN': ['', 1002, 1002]},
            {'NEWLINE': ['\n', 1079, 1080]},
            {'BEGIN': ['', 1080, 1080]},
            {'NEWLINE': ['\n', 1158, 1159]},
            {'BEGIN': ['', 1159, 1159]},
            {'NEWLINE': ['\n', 1167, 1168]},
            {'BEGIN': [' ', 1168, 1169]},
            {'UPPER_WORD_COLON': ['RESPIRATORY:', 1169, 1181]},
            {'TITLE_WORD': ['The', 1182, 1185]},
            {'NEWLINE': ['\n', 1238, 1239]},
            {'BEGIN': ['', 1239, 1239]},
            {'NEWLINE': ['\n', 1315, 1316]},
            {'BEGIN': ['', 1316, 1316]},
            {'NEWLINE': ['\n', 1343, 1344]},
            {'BEGIN': [' ', 1344, 1345]},
            {'UPPER_WORD_COLON': ['GASTROINTESTINAL:', 1345, 1362]},
            {'TITLE_WORD': ['The', 1363, 1366]},
            {'NEWLINE': ['\n', 1409, 1410]},
            {'BEGIN': ['', 1410, 1410]},
            {'NEWLINE': ['\n', 1487, 1488]},
            {'BEGIN': ['', 1488, 1488]},
            {'NEWLINE': ['\n', 1564, 1565]},
            {'BEGIN': ['', 1565, 1565]},
            {'NEWLINE': ['\n', 1641, 1642]},
            {'BEGIN': [' ', 1642, 1643]},
            {'UPPER_WORD_COLON': ['GENITOURINARY:', 1643, 1657]},
            {'TITLE_WORD': ['The', 1658, 1661]},
            {'NEWLINE': ['\n', 1713, 1714]},
            {'BEGIN': ['', 1714, 1714]},
            {'NEWLINE': ['\n', 1789, 1790]},
            {'BEGIN': ['', 1790, 1790]},
            {'NEWLINE': ['\n', 1865, 1866]},
            {'BEGIN': ['', 1866, 1866]},
            {'NEWLINE': ['\n', 1940, 1941]},
            {'BEGIN': ['', 1941, 1941]},
            {'NEWLINE': ['\n', 2021, 2022]},
            {'BEGIN': [' ', 2022, 2023]},
            {'UPPER_WORD_COLON': ['MUSCULOSKELETAL:', 2023, 2039]},
            {'TITLE_WORD': ['The', 2040, 2043]},
            {'NEWLINE': ['\n', 2094, 2095]},
            {'TITLE_WORD': ['No', 2095, 2097]},
            {'TITLE_WORD': ['No', 2120, 2122]},
            {'TITLE_WORD': ['No', 2154, 2156]},
            {'NEWLINE': ['\n', 2172, 2173]},
            {'BEGIN': ['', 2173, 2173]},
            {'NEWLINE': ['\n', 2225, 2226]},
            {'BEGIN': [' ', 2226, 2227]},
            {'UPPER_WORD': ['SKIN', 2227, 2231]},
            {'UPPER_WORD': ['AND', 2232, 2235]},
            {'UPPER_WORD_COLON': ['BREASTS:', 2236, 2244]},
            {'TITLE_WORD': ['The', 2245, 2248]},
            {'NEWLINE': ['\n', 2297, 2298]},
            {'BEGIN': ['', 2298, 2298]},
            {'NEWLINE': ['\n', 2373, 2374]},
            {'BEGIN': ['', 2374, 2374]},
            {'NEWLINE': ['\n', 2450, 2451]},
            {'BEGIN': ['', 2451, 2451]},
            {'NEWLINE': ['\n', 2473, 2474]},
            {'BEGIN': [' ', 2474, 2475]},
            {'UPPER_WORD_COLON': ['NEUROLOGIC:', 2475, 2486]},
            {'TITLE_WORD': ['The', 2487, 2490]},
            {'NEWLINE': ['\n', 2543, 2544]},
            {'BEGIN': ['', 2544, 2544]},
            {'NEWLINE': ['\n', 2618, 2619]},
            {'BEGIN': ['', 2619, 2619]},
            {'NEWLINE': ['\n', 2633, 2634]},
            {'BEGIN': [' ', 2634, 2635]},
            {'UPPER_WORD_COLON': ['PSYCHIATRIC:', 2635, 2647]},
            {'TITLE_WORD': ['The', 2648, 2651]},
            {'NEWLINE': ['\n', 2703, 2704]},
            {'BEGIN': ['', 2704, 2704]},
            {'NEWLINE': ['\n', 2771, 2772]},
            {'BEGIN': ['', 2772, 2772]},
            {'NEWLINE': ['\n', 2810, 2811]},
            {'BEGIN': [' ', 2811, 2812]},
            {'UPPER_WORD_COLON': ['ENDOCRINE:', 2812, 2822]},
            {'TITLE_WORD': ['The', 2823, 2826]},
            {'NEWLINE': ['\n', 2881, 2882]},
            {'BEGIN': ['', 2882, 2882]},
            {'NEWLINE': ['\n', 2954, 2955]},
            {'BEGIN': ['', 2955, 2955]},
            {'NEWLINE': ['\n', 2981, 2982]},
            {'BEGIN': [' ', 2982, 2983]},
            {'UPPER_WORD': ['HEMATOLOGIC', 2983, 2994]},
            {'UPPER_WORD_COLON': ['LYMPHATIC:', 2995, 3005]},
            {'TITLE_WORD': ['The', 3006, 3009]},
            {'NEWLINE': ['\n', 3053, 3054]},
            {'BEGIN': ['', 3054, 3054]},
            {'NEWLINE': ['\n', 3074, 3075]},
            {'BEGIN': [' ', 3075, 3076]},
            {'UPPER_WORD': ['ALLERGIC', 3076, 3084]},
            {'UPPER_WORD_COLON': ['IMMUNOLOGIC:', 3085, 3097]},
            {'TITLE_WORD': ['The', 3098, 3101]},
            {'NEWLINE': ['\n', 3139, 3140]},
            {'BEGIN': ['', 3140, 3140]}
        ]

        found_matches = Sectionizer().match_sectionizer(TEST_TEXT)

        for found_match in found_matches:
            key, value = list(found_match.items())[0]
            with self.subTest(pattern=key, parsed_value=value):
                self.assertTrue(found_match in expected_matches,
                                f"Match not found in expected values for pattern {key}.")

        self.assertEqual(len(found_matches), len(expected_matches),
                         "Count of found matches not equal to expected.")
