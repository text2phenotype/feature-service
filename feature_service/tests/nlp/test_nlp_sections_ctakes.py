import os
import unittest

from text2phenotype.ccda import ccda
from text2phenotype.common.errors import CCDAError
from text2phenotype.common.log import logger
from text2phenotype.common import common

from feature_service.nlp import ctakes_sectionizer
from feature_service.feature_service_env import FeatureServiceEnv


class TestNLPSectionsCTAKES(unittest.TestCase):

    def test_get_section_aspect_map_ctakes(self):
        """
        Test that we can build a {section:aspect} map from cTAKES.
        Note: this is most useful for section classification
        """
        common.write_json(
            ctakes_sectionizer.get_section_aspect_map_ctakes(),
            os.path.join(FeatureServiceEnv.DATA_ROOT.value, 'ccda', 'section_aspect_map_ctakes.json'))

    def test_section_is_mapped(self):
        """
        Test that every section in the cTAKES section list is supported by Text2phenotype.
        """
        known_sections = ccda.section_template_map.keys()
        known_documents = [entry.value for entry in ccda.DocumentType]

        for line in ctakes_sectionizer.__ctakes_sections__.splitlines():
            cols = line.split(',')
            if len(cols) > 1:
                code = cols[1]

                logger.debug('code [%s] line [%s]' % (code, line))

                if code not in known_documents:
                    if code not in known_sections:
                        raise CCDAError('section not known [ %s ] complete line is %s' % (code, line))
