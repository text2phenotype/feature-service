import datetime
import unittest

from text2phenotype.common.dates import parse_dates


TEST_TEXT = """Until 11:00PM, the evening of
11/27/87, when she suddenly awoke from
opathy and cerebral palsy. On 04/07/1988,
he underwent heart catheteri
non-Hodgkin 's lymphoma. From 03-29-88 to
08-02-1988, he received six
o my office for evaluation on 12/2010, and he was found to ha
recurred and was excised 09/84. There was
regrowth of this
to February 01,
2007, but has been discontin
May of 1988 
12. What is today's date? "July 21st, 2005."  
13. In what town
  and without contrast done on January
2007, showed hemorrhagic les 
   ation 3 times a day. However, June 20, he was seen in the ER,
 um of 3.9. Glucose was 213 on 23rd of September
2007.
ph node resection in the neck 24 April and biopsy of a\ntumor in the 

ASSESSMENT:
The patient was born on 03-04-1985 and was first seen by the PCP on 03-04-1986.
The patient was born on 03/04/1985 and was first seen by the PCP on 03-04-1986.
The patient was born on 1985-03-04 and was first seen by the PCP on 03-04-1986.
The patient was born on 1985/03/04 and was first seen by the PCP on 03-04-1986.
The patient was born on March 4, 1985 and was first seen by the PCP on 03-04-1986.
The patient was born on March 04, 1985 and was first seen by the PCP on 03-04-1986.
The patient was born on March fourth 1985 and was first seen by the PCP on 03-04-1986.
"""


class TestBiomed495(unittest.TestCase):

    def test_parse_dates(self):

        expected_matches = [(datetime.datetime(1987, 11, 27, 0, 0), (30, 39)),
                            (datetime.datetime(1988, 4, 7, 0, 0), (99, 110)),
                            (datetime.datetime(1988, 3, 29, 0, 0), (170, 179)),
                            (datetime.datetime(1988, 8, 2, 0, 0), (182, 193)),
                            (datetime.datetime(2010, 12, 1, 0, 0), (240, 248)),
                            (datetime.datetime(1984, 9, 1, 0, 0), (297, 303)),
                            (datetime.datetime(2007, 2, 1, 0, 0), (334, 352)),
                            (datetime.datetime(1988, 5, 1, 0, 0), (376, 388)),
                            (datetime.datetime(2005, 7, 21, 0, 0), (416, 432)),
                            (datetime.datetime(2007, 1, 1, 0, 0), (484, 497)),
                            (datetime.datetime(datetime.MAXYEAR, 6, 20, 0, 0), (555, 563)),
                            (datetime.datetime(2007, 9, 23, 0, 0), (618, 641)),
                            (datetime.datetime(datetime.MAXYEAR, 4, 24, 0, 0), (672, 681)),
                            (datetime.datetime(1985, 3, 4, 0, 0), (748, 759)),
                            (datetime.datetime(1986, 3, 4, 0, 0), (792, 803)),
                            (datetime.datetime(1985, 3, 4, 0, 0), (828, 839)),
                            (datetime.datetime(1986, 3, 4, 0, 0), (872, 883)),
                            (datetime.datetime(1985, 3, 4, 0, 0), (908, 919)),
                            (datetime.datetime(1986, 3, 4, 0, 0), (952, 963)),
                            (datetime.datetime(1985, 3, 4, 0, 0), (988, 999)),
                            (datetime.datetime(1986, 3, 4, 0, 0), (1032, 1043)),
                            (datetime.datetime(1985, 3, 4, 0, 0), (1068, 1082)),
                            (datetime.datetime(1986, 3, 4, 0, 0), (1115, 1126)),
                            (datetime.datetime(1985, 3, 4, 0, 0), (1151, 1166)),
                            (datetime.datetime(1986, 3, 4, 0, 0), (1199, 1210)),
                            (datetime.datetime(1985, 3, 4, 0, 0), (1235, 1253)),
                            (datetime.datetime(1986, 3, 4, 0, 0), (1286, 1297))]

        found_matches = parse_dates(TEST_TEXT)

        for found_match in found_matches:
            date, position = found_match
            with self.subTest(pattern=date, position=position):
                self.assertIn(found_match, expected_matches, f'Match not found in expected values for date {date}.')

        self.assertEqual(len(found_matches), len(expected_matches), 'Count of found matches not equal to expected.')
