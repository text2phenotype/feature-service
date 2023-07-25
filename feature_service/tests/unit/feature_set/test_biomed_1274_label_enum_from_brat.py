import unittest

from text2phenotype.constants.features.label_types import (
    AllergyLabel,
    CancerLabel,
    DemographicEncounterLabel,
    DisabilityLabel,
    HeartDiseaseLabel,
    LabLabel,
    MedLabel,
    PHILabel,
    ProblemLabel,
    SignSymptomLabel,
)


class TestBiomed1273(unittest.TestCase):
    INVALID_TOKEN = 'afjdoa'

    def test_phi_label_enum_invalid_token(self):
        brat_value = PHILabel.from_brat(self.INVALID_TOKEN)
        self.assertEqual(brat_value, PHILabel.na)

    def test_phi_label_valid_upper_token(self):
        brat_value = PHILabel.from_brat(PHILabel.na.name.upper())
        self.assertEqual(brat_value, PHILabel.na)

    def test_phi_location(self):
        self.assertEqual(PHILabel.from_brat('location'), PHILabel.street)

    def test_med_label_invalid_token(self):
        self.assertEqual(MedLabel.from_brat(self.INVALID_TOKEN), MedLabel.na)

    def test_med_label_valid_token(self):
        self.assertEqual(MedLabel.from_brat(MedLabel.med.name), MedLabel.med)

    def test_med_label_medication(self):
        self.assertEqual(MedLabel.from_brat('medication'), MedLabel.med)

    def test_demographic_invalid_token(self):
        self.assertEqual(DemographicEncounterLabel.from_brat(self.INVALID_TOKEN), DemographicEncounterLabel.na)

    def test_demographic_valid_token(self):
        self.assertEqual(DemographicEncounterLabel.from_brat(DemographicEncounterLabel.pat_first.name.upper()),
                         DemographicEncounterLabel.pat_first)

    def test_lab_invalid_token_from_brat(self):
        self.assertEqual(LabLabel.from_brat(self.INVALID_TOKEN), LabLabel.na)

    def test_lab_valid_from_brat(self):
        self.assertEqual(LabLabel.from_brat(LabLabel.lab.name.upper()), LabLabel.lab)

    def test_allergy_invalid_from_brat(self):
        self.assertEqual(AllergyLabel.from_brat(self.INVALID_TOKEN), AllergyLabel.na)

    def test_allergy_valid_from_brat(self):
        self.assertEqual(AllergyLabel.from_brat(AllergyLabel.allergy.name), AllergyLabel.allergy)

    def test_sign_symptom_invalid_from_brat(self):
        self.assertEqual(SignSymptomLabel.from_brat(self.INVALID_TOKEN), SignSymptomLabel.na)

    def test_sign_symptom_valid_from_brat(self):
        self.assertEqual(SignSymptomLabel.from_brat(SignSymptomLabel.signsymptom.name), SignSymptomLabel.signsymptom)

    def test_problem_invalid_from_brat(self):
        self.assertEqual(ProblemLabel.from_brat(self.INVALID_TOKEN), ProblemLabel.na)

    def test_problem_valid_from_brat(self):
        self.assertEqual(ProblemLabel.from_brat(ProblemLabel.problem.name.upper()), ProblemLabel.problem)

    def test_disability_label_invalid_token(self):
        self.assertEqual(DisabilityLabel.from_brat(self.INVALID_TOKEN), DisabilityLabel.na)

    def test_disability_label_valid_from_brat(self):
        self.assertEqual(DisabilityLabel.from_brat(DisabilityLabel.signsymptom.name), DisabilityLabel.signsymptom)

    def test_cancer_label_invalid_from_brat(self):
        self.assertEqual(CancerLabel.from_brat(self.INVALID_TOKEN), CancerLabel.na)

    def test_cancer_valid_from_brat(self):
        self.assertEqual(CancerLabel.from_brat(CancerLabel.topography_primary.name), CancerLabel.topography_primary)

    def test_hdrf_label_invalid_from_brat(self):
        self.assertEqual(HeartDiseaseLabel.from_brat(self.INVALID_TOKEN), HeartDiseaseLabel.na)

    def test_hdrf_label_valid_from_brat(self):
        self.assertEqual(HeartDiseaseLabel.from_brat(HeartDiseaseLabel.hypertension.name),
                         HeartDiseaseLabel.hypertension)
