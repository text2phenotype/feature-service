import unittest
from text2phenotype.common import speech


class TestNLTKSpeech(unittest.TestCase):
    def test_example_1(self):
        INPUT = """
...
.
.
..
.
"
1.'.
'"griiii
Shannon Fee, MD 32/09/12 1133
Shannon Fee, MD 09/32/12 1133
Ordering Provider."""

        tokens = speech.tokenize(INPUT)  # now a list of token dictionary


    def test_example_2(self):
        INPUT = """!..HISHD-TG .....OHDSAOIHD- 
w 
Secondary 
wwwwww..........
15 -TG
Diagnosis -..."""""""'"'"''''..i.nir.nw."'"""""""" """

        tokens = speech.tokenize(INPUT)