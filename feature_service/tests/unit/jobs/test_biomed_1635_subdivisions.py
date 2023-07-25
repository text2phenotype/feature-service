import unittest

from feature_service.jobs.job_metadata import Subdivisions


class TestSubdivisionPoints(unittest.TestCase):
    def test_subdivision_default(self):
        meta = Subdivisions({'train': .8, 'test': .2})
        subdivision_probs = meta.subdivision_split_points
        self.assertDictEqual(subdivision_probs, {'train': (0, .8), 'test': (.8, 1)})

    def test_subdivision_from_list(self):
        meta = Subdivisions(['a', 'b', 'c', 'd'])
        subdivision_probs = meta.subdivision_split_points
        self.assertDictEqual(subdivision_probs, {'a': (0, .25), 'b': (.25, .5), 'c': (.5, .75), 'd':(.75, 1)})

    def test_subdivision_from_weighted_list(self):
        meta = Subdivisions({'a': 4, 'b': 1})
        subdivision_probs = meta.subdivision_split_points
        self.assertDictEqual(subdivision_probs, {'a': (0, .8), 'b': (.8, 1)})

    def test_subdivisions_weights_from_doc_count(self):
        entry = {'a': 4, 'b': 1}
        subdivis = Subdivisions(entry)
        subdivis.create_subdivision_expect_doc_count(5)
        self.assertDictEqual(entry, subdivis.subdivision_doc_count)

        subdivis.create_subdivision_expect_doc_count(15)
        self.assertDictEqual(subdivis.subdivision_doc_count, {'a': 12, 'b': 3})

    def test_updating_weights(self):
        entry = {'a': 4, 'b': 1}
        subdivis = Subdivisions(entry)
        subdivis.create_subdivision_expect_doc_count(5)
        subdivis.reduce_exp_doc_count('a')
        self.assertEqual(subdivis.subdivision_doc_count, {'a': 3, 'b': 1})
        self.assertEqual(subdivis.subdivision_split_points, {'a': (0, .75), 'b': (.75, 1)})
        subdivis.reduce_exp_doc_count('b')
        self.assertEqual(subdivis.subdivision_doc_count, {'a': 3, 'b': 0})
        self.assertEqual(subdivis.subdivision_split_points, {'a': (0, 1), 'b': (1, 1)})

    def test_non_even_weights(self):
        subdivis = Subdivisions(['a', 'b', 'c', 'd', 'e'])
        subdivis.create_subdivision_expect_doc_count(6)
        expected = {'a': 1.2, 'b': 1.2, 'c': 1.2, 'd': 1.2, 'e': 1.2}
        self.assertDictEqual(expected, subdivis.subdivision_doc_count)

        subdivis.reduce_exp_doc_count('a')
        probs = subdivis.subdivision_probs
        expected = 1.2/(1.2*4+.2)
        for i in ['b', 'c', 'd', 'e']:
            self.assertEqual(probs[i], expected)

    def test_create_multiple(self):
        entry = {'a': 4, 'b': 1}
        subdivis = Subdivisions(entry)
        subdiv_default_probs = {"a": .8, "b": .2}
        subdivis.create_subdivision_expect_doc_count(5)
        for i in range(4):
            subdivis.reduce_exp_doc_count('a')
        subdivis.reduce_exp_doc_count('b')
        self.assertEqual(subdivis.subdivision_doc_count, {'a': 0, 'b': 0})
        subdivis.create_subdivision_expect_doc_count(10)
        self.assertEqual(subdivis.default_subdivision_probs, subdiv_default_probs)
        self.assertEqual(subdivis.subdivision_doc_count, {'a': 8, 'b': 2})