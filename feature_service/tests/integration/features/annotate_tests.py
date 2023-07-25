from typing import List, Set
import unittest

from feature_service.features.feature import Feature
from feature_service.feature_set import annotation, vectorization


class AnnotateTestsBase(unittest.TestCase):

    TEST_INPUT_DVAUGHAN_SUBSET = '''ViSolve Clinic
David Vaughan
Patient Notes:
http://demo.visolve.com/openemr-text2phenotype/interface/patient_file/report/custom_report.php?p...
7/21/2017
Generated on: 2017-07-21
2017-07-20: Discharge Summary DISCHARGE DIAGNOSES: 1. End-stage renal disease, on hemodialysis. 2. History 
of T9 vertebral fracture. 3. Diskitis. 4. Thrombocytopenia. 5. Congestive heart failure with ejection fraction of 
approximately 30%. 6. Diabetes, type 2. 7. Protein malnourishment. 8. History of anemia. HISTORY AND HOSPITAL 
WhoName:Mr. David K. VaughanExternal ID:601-60-0606
COURSE: The patient is a 77-year-old white male who presented to Hospital of Bossier on April 14, 2008 with fever 
and severe lower back pain and severe weakness. The patient was found to have lumbar Diskitis that requires extensive 
DOB:1940-07-18
Sex:Male
antibiotic therapy, which required hospitalization due to his dialysis. He also needed increase the frequency of his 
dialysis due to worsening renal function. Dialysis time was extended and frequency was increased to three times per 
week. He needed to begin active rehabilitation. The patient tolerated his medication well and he was going through 
rehab fairly well without any significant troubles. He did have some bouts of issues with constipation on and off 
throughout his hospitalization, but this seemed to come under control with more aggressive management. The patient 
had remained afebrile. He did also have a bout with some episodic confusion problems, which appeared to be more of a 
sundowner-type of a problem, but this too cleared with his stay here at Promise. On the day of discharge, on May 9, 
2008, the patient was in good spirits, was very clear and lucid. He denied any complaints of pain. He did have some 
trouble with sleep at night at times, but I think this was mainly tied into the fact that he sleeps a lot during the day. The 
patient has increased his appetite some and has been eating some. His vital signs remain stable. His blood pressure on 
discharge was 126/63, heart rate is 80, respiratory rate of 20 and temperature was 98.3. PPD was negative. An SMS 
PATIENT:Vaughan, David - 07/18/1940 Generated on 2017-07-21 - ViSolve Clinic 000-000-0000
, 000-000-0000 '''

    TEST_INPUT_CAROLYN = '''Page 1 of 3
PATIENT:Blose, Carolyn - 07/29/1932 Generated on 2017-07-21 - ViSolve Clinic 000-000-0000
ViSolve Clinic
000-000-0000
Carolyn Blose
Generated on: 2017-07-21
Patient Data:
Who Name: Mr. Carolyn V. Blose External ID: 530-79-5301
DOB: 1932-07-29
Sex: Female
History Data:
General Risk Factors:
Hypertension
Exams/Tests:
Lifestyle Tobacco:
Never smoker ( SNOMED-CT:266919005 ) nonsmoker Status: Never
Coffee:
Alcohol:
not consume alcohol
Recreational Drugs: No history of recreational drug use.
Counseling:
Exercise Patterns:
Hazardous Activities:
Insurance Data:
Primary Insurance Data:
Subscriber Date of Birth:
0000-00-00
Secondary Insurance Data:
Subscriber Date of Birth:
0000-00-00
Tertiary Insurance Data:
Subscriber Date of Birth:
0000-00-00
Billing Information:
Patient Immunization:
Patient Notes:
2017-07-19: Admitting diagnoses: Bloody diarrhea Shortness of breath congestive heart failure Discharge diagnosis:
Diverticulitis Valvular insufficiency Congestive Heart Failure HISTORY OF PRESENT ILLNESS: The patient is an
84-year-old female admitted for evaluation of abdominal pain and bloody stools. The patient has colitis and also
diverticulitis, undergoing treatment. During the hospitalization, the patient complained of shortness of breath, which
http://demo.visolve.com/openemr-text2phenotype/interface/patient file/report/custom report.php?p... 7/21/2017
Page 2 of 3
worsened. The patient underwent an echocardiogram, which shows severe mitral regurgitation and also large pleural
effusion. Per the patient, she has limited activity level with shortness of breath for many years. She also was told that
she has a heart murmur, which was not followed through for a diagnosis. CORONARY RISK FACTORS: History of
hypertension, no history of diabetes mellitus, nonsmoker, cholesterol status unclear, no prior history of coronary artery
disease, and family history noncontributory. FAMILY HISTORY: Nonsignificant. PAST SURGICAL HISTORY: No
major surgery. MEDICATIONS: Presently on Lasix, potassium supplementation, Levaquin, hydralazine 10 mg b.i.d.,
antibiotic treatments, and thyroid supplementation. ALLERGIES: AMBIEN, CARDIZEM, AND IBUPROFEN.
PERSONAL HISTORY: She is a nonsmoker. Does not consume alcohol. No history of recreational drug use. PAST
MEDICAL HISTORY: Basically GI pathology with diverticulitis, colitis, hypothyroidism, arthritis, questionable
hypertension, no prior history of coronary artery disease, and heart murmur. REVIEW OF SYSTEMS
CONSTITUTIONAL: Weakness, fatigue, and tiredness. HEENT: History of cataract, blurred vision, and hearing
impairment. CARDIOVASCULAR: Shortness of breath and heart murmur. No coronary artery disease.
RESPIRATORY: Shortness of breath. No pneumonia or valley fever. GASTROINTESTINAL: No nausea, vomiting,
hematemesis, or melena. UROLOGICAL: No frequency or urgency. MUSCULOSKELETAL: Arthritis and severe
muscle weakness. SKIN: Nonsignificant. NEUROLOGICAL: No TIA or CVA. No seizure disorder.
ENDOCRINE/HEMATOLOGICAL: As above. PHYSICAL EXAMINATION VITAL SIGNS: Pulse of 84, blood
pressure of 168/74, afebrile, and respiratory rate 16 per minute. HEENT/NECK: Head is atraumatic and normocephalic.
Neck veins flat. No significant carotid bruits appreciated. LUNGS: Air entry bilaterally fair. No obvious rales or
wheezes. HEART: PMI displaced. S1, S2 with systolic murmur at the precordium, grade 2/6. ABDOMEN: Soft and
nontender. EXTREMITIES: Chronic skin changes. Feeble pulses distally. No clubbing or cyanosis. DIAGNOSTIC
DATA: EKG: Normal sinus rhythm. No acute ST-T changes. Echocardiogram was reviewed showing severe mitral
regurgitation. LABORATORY DATA: H&H 13 and 39. BUN and creatinine within normal limits. Potassium within
normal limits. BNP 9290. IMPRESSION: 1. The patient admitted for gastrointestinal pathology, under working
treatment. 2. History of prior heart murmur with Echocardiogram findings as above. Basically revealed normal left
ventricular function with left atrial enlargement, large pleural effusion, and severe mitral regurgitation and tricuspid
regurgitation. Discharge Recommendations: 1. Finish antibiotics, High fiber diet for diverticulitis. PCP follow up in 30
days 2. From cardiac standpoint, conservative treatment. Possibility of a transesophageal echocardiogram to assess
valvular insufficiency adequately well discussed extensively. After extensive discussion, given her age 86, limited
activity level, and no intention of undergoing any treatment in this regard from a surgical standpoint, the patient does
not wish to proceed with a transesophageal echocardiogram. 3. Based on the above findings, we will treat her cardiac
disease medically with ACE inhibitors and diuretics and see how she fares. She has a normal LV function.
Patient Transactions:
::::::::::::::::::::1111111111111111111111111110
Patient Communication sent:
Recurrent Appointments:
None
Issues
Allergies:
AMBIEN:
CARDIZEM:
IBUPROFEN:
Medications:
Lasix:
potassium supplementation:
Levaquin:
hydralazine 10 mg b.i.d.:
antibiotic treatments:
thyroid supplementation:
.....................................................................................................................................
http://demo.visolve.com/openemr-text2phenotype/interface/patient file/report/custom report.php?p... 7/21/2017
Page 3 of 3
New Patient Encounter
(2017-07-19) Provider: Administrator Administrator
Facility: ViSolve Clinic
Reason: HISTORY OF PRESENT ILLNESS: The patient is an 84-year-old female admitted for evaluation of abdominal
pain and bloody stools. The patient has colitis and also diverticulitis, undergoing treatment. During the hospitalization, the
patient complained of shortness of breath, which worsened. The patient underwent an echocardiogram, which shows
severe mitral regurgitation and also large pleural effusion. Per the patient, she has limited activity level with shortness of
breath for many years. She also was told that she has a heart murmur, which was not followed through for a diagnosis.
Review Of Systems
(2017-07-19)
Weakness: Fatigue:
YES
YES
Shortness Of Breath: History Murmur:
YES
YES
Vomiting:
YES
Hematemesis:
YES
TIA: NO
Vitals
(2017-07-19)
Blood Pressure: 168/74 Pulse: 84 per min Respiration: 16 per min
Review of Systems Checks
(2017-07-19)
Cataracts: yes Blurred Vision: yes Shortness Of Breath: yes
Signature:
http://demo.visolve.com/openemr-text2phenotype/interface/patient file/report/custom report.php?p... 7/21/2017 '''

    @staticmethod
    def find_match(match: str, items: list) -> bool:
        for item in items:
            dictionary = item[1][0]
            if match in dictionary:
                return True

        return False

    @staticmethod
    def find_polarity_type_match(match: str, items: list, feature_name: str):
        for item in items:
            list_type = item[1][0]
            if list_type == feature_name:
                return True

        return False

    @staticmethod
    def find_match_count(match: str, items: list) -> int:
        count = 0
        for item in items:
            dictionary = item[1][0]
            if match in dictionary:
                count += 1

        return count

    @staticmethod
    def find_match_key_value(k: str, v: str, items: list) -> bool:
        for item in items:
            dictionary = item[1][0]
            if k in dictionary:
                if dictionary[k] == v:
                    return True

        return False


class MatchHintVectorizeBase(unittest.TestCase):
    """Base functions for vectorization tests of MatchHint subclasses"""
    def _test_vectorize(self, token: str, feature: Feature, one_hot_indices: List[int]):
        """
        Run a vectorization test against a single token input.
        :param token: The token string to vectorize.
        :param feature: The feature to test.
        :param one_hot_indices: The indices expected to be 1.
        """
        from feature_service.feature_set import annotation, vectorization

        machine_annotation = annotation.annotate_text(token, feature_types=[feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation, feature_types=[feature.feature_type])
        observed = vectors.output_dict[feature.feature_type][0]
        if observed is None:
            observed = vectors.defaults[feature.feature_type]

        expected = [0] * len(feature.CONST_KEYS)
        for i in one_hot_indices:
            expected[i] = 1

        self.assertListEqual(expected, observed)

    def _test_vectorize_all_definitions(self, feature: Feature, exclusions: Set[str] = None):
        """
        Run a vectorization test against all defined terms.
        :param feature: The feature to test.
        :param exclusions: Set of definitions to skip testing.
        """
        for key, values in feature.DEFINITIONS.items():
            if exclusions and key in exclusions:
                continue

            machine_annotation = annotation.annotate_text(values[0], feature_types=[feature.feature_type])

            vectors = vectorization.vectorize_from_annotations(machine_annotation, feature_types=[feature.feature_type])
            observed = vectors.output_dict[feature.feature_type][0]
            if observed is None:
                observed = vectors.defaults[feature.feature_type]

            expected = [0] * len(feature.CONST_KEYS)
            expected[feature.CONST_KEYS[key]] = 1

            self.assertListEqual(expected, observed, msg=f'Vectorization failed for {key}')

    def _test_vectorize_no_match(self, feature: Feature):
        """
        Run a vectorization test against all defined terms.
        :param feature: The feature to test.
        """
        machine_annotation = annotation.annotate_text('//a23-----pasidvhankljhk', feature_types=[feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation, feature_types=[feature.feature_type])

        self.assertIsNone(vectors.output_dict[feature.feature_type][0])
