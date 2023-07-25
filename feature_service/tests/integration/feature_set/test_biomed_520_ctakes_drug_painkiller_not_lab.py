import unittest

from feature_service.nlp.nlp_reader import DrugReader, HepcLabReader

TEXT_MEDS = """
DISCHARGE MEDICATIONS :
Premarin 0.625 q.d. , Proventil Inhaler two puffs q.i.d. , Beclovent four puffs b.i.d. , Colace 100 mg p.o. t.i.d. , MS Contin 30 mg p.o. t.i.d. , Elavil 25 mg p.o. q.h.s. , Trilisate 750 mg p.o. b.i.d. , MS Elixir 100 mg p.o. q.2h. p.r.n. , Robitussin with Codeine 5 cc p.o. q.2h. , and home O2 two liters via nasal prong with increase to four liters as needed for symptoms p.r.n.
"""


class TestBiomed520(unittest.TestCase):

    def test_painkiller_ms_contin_is_medication(self):
        self.assertIn('MS Contin', DrugReader(TEXT_MEDS).list_result_text())

    def test_painkiller_ms_contin_is_not_lab(self):

        matches = HepcLabReader(TEXT_MEDS).list_result_text()

        self.assertNotIn('MS Contin', matches)
        self.assertTrue('MS' not in matches)

        self.assertEqual(0, len(matches))
