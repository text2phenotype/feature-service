import datetime
import unittest

from feature_service.features import DateComprehension


class DateComprehensionAnnotateTests(unittest.TestCase):

    TEST_INPUT = 'Generated on: 2017-07-21 ' \
                 'WhoName:Mr. Carolyn V. BloseExternal ID:530-79-5301 ' \
                 'DOB:1932-07-29 ' \
                 'Sex:Female' \
                 '2017-07-19: Admitting diagnoses: Bloody diarrhea Shortness of breath congestive heart failure ' \
                 'Discharge diagnosis: '

    def test_date_comprehension_annotate_simple(self):

        target = DateComprehension()
        actual = list(target.annotate("Patients DOB: 08/01/1950"))

        # 1 date, ensure the character positions are correct.
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0][0][0], 14)
        self.assertEqual(actual[0][0][1], 24)

    def test_date_comprehension_annotate_3_dates(self):

        target = DateComprehension()
        actual = list(target.annotate(self.TEST_INPUT))

        # 3 dates
        self.assertEqual(len(actual), 3, f"DateComprehension annotate() expected 3 dates to be parsed from input but "
                                         f"got {str(len(actual))}")
        n = [0,0,0]
        for i in range(len(actual)):
            if actual[i][0][0] == 14:
                self.assertEqual(actual[i][0][1], 25)
                # 31038 days between 1932-07-29 & 2017-07-21
                self.assertEqual(actual[i][1][0]['first'], False)
                # this is the last date
                self.assertEqual(actual[i][1][0]['last'], True)
                n[0] = 1
            elif actual[i][0][0] == 81:
                # 2nd date is the dob
                self.assertEqual(actual[i][0][0], 81)
                self.assertEqual(actual[i][0][1], 92)

                self.assertEqual(actual[i][1][0]['first'], True)
                # 31038 days between 1932-07-29 & 2017-07-21
                self.assertEqual(actual[i][1][0]['last'], False)
                n[1] = 1

            elif actual[i][0][0] == 102:

                # 3rd date is the admission date
                self.assertEqual(actual[i][0][0], 102)
                self.assertEqual(actual[i][0][1], 113)
                # admitted 31036 days after birth date
                self.assertEqual(actual[i][1][0]['first'], False)
                # 2 days before the generated date
                self.assertEqual(actual[i][1][0]['last'], False)
                n[2] = 1

        self.assertEqual(n, [1, 1, 1])

