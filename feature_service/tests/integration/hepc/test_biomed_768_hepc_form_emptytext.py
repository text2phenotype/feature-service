import unittest

from feature_service.hep_c.form import autofill_hepc_form


class TestBiomed768(unittest.TestCase):

    def test_something_unimportant(self):
        autofill_hepc_form('Unimportant')

    def test_empty_string(self):
        autofill_hepc_form('')
