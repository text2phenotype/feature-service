import os
from typing import List
from lxml import etree, objectify

from text2phenotype.common import common

from feature_service.feature_service_env import FeatureServiceEnv

###############################################################################
#
# Parse XML
#
###############################################################################


def parse(i2b2_xml):
    """
    :param i2b2_xml: XML (either filepath or parsed Elements)
    :return: ElementTree
    """
    # if ccda_xml is already parsed, return...
    if isinstance(i2b2_xml, etree._ElementTree):
        return i2b2_xml

    parser = etree.XMLParser(remove_comments=True)
    return objectify.parse(i2b2_xml, parser=parser)


def get_root(i2b2_xml):
    """
    Get XML root of i2b2 XML file
    :param i2b2_xml: XML (either filepath or parsed Elements)
    :return: ElementTree XML parsed
    """
    return parse(i2b2_xml).getroot()


def get_text(i2b2_xml):
    """
    Get text from i2b2 document
    :param i2b2_xml:  XML (either filepath or parsed Elements)
    :return: str
    """
    for _child in get_root(i2b2_xml).getchildren():
        if 'TEXT' == _child.tag:
            return _child.text


def get_tags(i2b2_xml):
    """
    tags -- Get Human Expert annotations
    :param i2b2_xml: XML (either filepath or parsed Elements)
    :return: dict() of
    """
    return [_phi.attrib for _phi in get_raw_tags(i2b2_xml)]


def get_raw_tags(i2b2_xml):
    """
    tags -- Get Human Expert annotations
    :param i2b2_xml: XML (either filepath or parsed Elements)
    :return: dict() of
    """
    for _child in get_root(i2b2_xml).getchildren():
        if 'TAGS' == _child.tag:
            return _child.getchildren()


###############################################################################
#
# Get and process samples: training/testing
#
###############################################################################


def get_training_files(folders: List[str] = None, file_type='.xml'):
    """
    Get I2B2 Training sample files
    """
    train_files = list()

    if not folders:
        # if folders is not provided, get the default folders for training
        folders = ['2018-11-27/training-PHI-Gold-Set1', '2018-11-27/training-PHI-Gold-Set2']

    for train_dir in folders:
        train_files += common.get_file_list(os.path.join(
            os.path.join(FeatureServiceEnv.DATA_ROOT.value, 'I2B2', '2014 De-identification and Heart Disease Risk Factors Challenge'),
            train_dir), file_type)
    return train_files


def get_testing_files(folders: List[str] = None, file_type: str = '.xml'):
    """
    Get I2B2 testing sample files
    """
    test_files = list()
    if not folders:
        # if folder is not provided, get the default folder for testing
        folders = ['2018-11-27/testing-PHI-Gold-fixed']

    for test_dir in folders:
        test_files += common.get_file_list(os.path.join(
            os.path.join(FeatureServiceEnv.DATA_ROOT.value, 'I2B2', '2014 De-identification and Heart Disease Risk Factors Challenge'),
            test_dir), file_type)

    return test_files
