import os
import timeit
import unittest
from feature_service.features.sectionizer import Sectionizer


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


class TestBiomed416SectionizerSpeed(unittest.TestCase):

    def test_sectionizer(self):
        with open(os.path.join(MTSAMPLES_DIR, 'neuropsychological-evaluation-4.txt-clean.txt'), 'r') as f:
            test_target = Sectionizer()
            wrapped_sectionizer = wrapper(test_target.match_sectionizer, f.read())
            self.assertLess(timeit.timeit(wrapped_sectionizer, number=100), 6)
