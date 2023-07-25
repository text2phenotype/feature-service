import unittest

from feature_service.nlp.nlp_reader import HepcLabReader


class TestBiomed247(unittest.TestCase):

    def test_lab_value_normal(self):

        text = """
        LABORATORY DATA: H&H 13 and 39. BUN and creatinine within normal limits. 
        Potassium within normal limits. BNP 9290.         
        """
        cui_bun = 'C0005845'
        cui_creatinine = 'C0201975'

        self.assertNormal(text, cui_bun)
        self.assertNormal(text, cui_creatinine)

    def test_lab_value_normal_bun(self):
        cui = 'C0005845'
        self.assertNormal("BUN and creatinine within normal limits", cui)
        self.assertNormal("BUN within normal limits", cui)
        self.assertNormal("BUN is normal", cui)

    def test_lab_value_normal_creatinine(self):

        cui = 'C0201975'
        self.assertNormal("Creatinine within normal limits", cui)
        self.assertNormal("BUN and creatinine within normal limits", cui)
        self.assertNormal("Creatinine and BUN within normal limits", cui)

    def assertNormal(self, text, cui, normal='normal'):
        """
        :param text:
        :param cui:
        :param normal:
        :return:
        """
        reader = HepcLabReader(text)

        self.assertIn(cui, reader.list_concept_cuis())
        self.assertTrue(normal, reader.list_lab_values())
