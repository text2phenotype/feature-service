import unittest

from feature_service.features.sectionizer import Sectionizer

TEST_TEXT = """
http://www.test.com/developertest/news/test.rss

http://someportal.com:10040/wps/proxy/http/www.test.com/developertest/news/test.rss

https://someportal.com:1234/sitemap

http://myportal.com:10040/wps/proxy/http/myotherportal.com%3a1234/sitemap

http://www-01.test.com/software/swnews/swnews.nsf/swnewsrss?openview&SomeCategory=test

http://myportal.com:10040/wps/ibmsoftwarenews/swnews.nsf/swnewsrss?openview&SomeCategory=test

http://example.com

https://example.com

http://www.example.com

https://www.example.com

https://www.example.com/some-url-with-id-12346546789/

ftp://exampletest.example.edu/

https://en.wikipedia.org/wiki/Internet#Terminology

"""


class TestBiomed603(unittest.TestCase):

    def test_sectionizer(self):

        expected_matches = [
            {'URL': ['http://www.test.com/developertest/news/test.rss', 1, 48]},
            {'URL': ['http://someportal.com:10040/wps/proxy/http/www.test.com/developertest/news/test.rss', 50, 133]},
            {'URL': ['https://someportal.com:1234/sitemap', 135, 170]},
            {'URL': ['http://myportal.com:10040/wps/proxy/http/myotherportal.com%3a1234/sitemap', 172, 245]},
            {'URL': ['http://www-01.test.com/software/swnews/swnews.nsf/swnewsrss?openview&SomeCategory=test', 247, 333]},
            {'URL': ['http://myportal.com:10040/wps/ibmsoftwarenews/swnews.nsf/swnewsrss?openview&SomeCategory=test', 335, 428]},
            {'URL': ['http://example.com', 430, 448]},
            {'URL': ['https://example.com', 450, 469]},
            {'URL': ['http://www.example.com', 471, 493]},
            {'URL': ['https://www.example.com', 495, 518]},
            {'URL': ['https://www.example.com/some-url-with-id-12346546789/', 520, 573]},
            {'URL': ['ftp://exampletest.example.edu/', 575, 605]},
            {'URL': ['https://en.wikipedia.org/wiki/Internet#Terminology', 607, 657]}
        ]

        found_matches = Sectionizer().match_pattern(TEST_TEXT, "URL")

        for found_match in found_matches:
            key, value = list(found_match.items())[0]
            with self.subTest(pattern=key, parsed_value=value):
                self.assertTrue(found_match in expected_matches,
                                f"Match not found in expected values for pattern {key}.")

        self.assertEqual(len(found_matches), len(expected_matches),
                         "Count of found matches not equal to expected.")
