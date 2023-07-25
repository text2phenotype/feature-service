from lxml import (
    etree,
    objectify,
)
import os
import string

from text2phenotype.apiclients.feature_service import FeatureServiceClient
from text2phenotype.common import common
from text2phenotype.common.feature_data_parsing import overlap_ranges

from feature_service.feature_service_env import FeatureServiceEnv


# source: https://www.i2b2.org/NLP/DataSets/
I2B2_2006_DIR = os.path.join(FeatureServiceEnv.DATA_ROOT.value, 'I2B2', 'Data Set 1B De-identification')

TRAIN_DIR = os.path.join(I2B2_2006_DIR, 'train', 'surrogates_richen.zhang_2018-05-18_1526688362.423912')
TEST_DIR = os.path.join(I2B2_2006_DIR, 'test', 'surrogates_richen.zhang_2018-05-18_1526686657.604676')
TRAIN_XML = os.path.join(I2B2_2006_DIR, 'train', 'deid_surrogate_train_all_version2.xml')
TEST_XML = os.path.join(I2B2_2006_DIR, 'test', 'deid_surrogate_test_all_groundtruth_version2.xml')


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


def get_records(i2b2_xml):
    return get_root(i2b2_xml).getchildren()


def get_text(i2b2_xml):
    for _child in get_root(i2b2_xml).getchildren():
        if 'TEXT' == _child.tag:
            return _child.text


def get_tags(i2b2_xml):
    """
    tags -- Get Human Expert annotations
    :param i2b2_xml: XML (either filepath or parsed Elements)
    :return: dict() of
    """
    _tags = list()

    for _child in get_root(i2b2_xml).getchildren():
        if 'TAGS' == _child.tag:
            for _phi in _child.getchildren():
                _tags.append(_phi.attrib)

    return _tags


###############################################################################
#
# Tokenize
#
###############################################################################

def tokenize_tags(i2b2_xml):
    """
    tokenize -- PHI Human Expert annotations into a dictionary
    :param i2b2_xml: XML (either filepath or parsed Elements)
    :return: dict of PHI positions
    """
    res = dict()

    for _tag in get_tags(i2b2_xml):
        _index = range(int(_tag['start']), int(_tag['end']))
        _text = _tag['text']
        _phi = _tag['TYPE']
        res[_index] = {'phi': _phi, 'text': _text}

    return res


def annotate_xml(i2b2_xml):
    """
    :param i2b2_xml: XML (either filepath or parsed Elements)
    :return: list of dictionary
    """
    tags = tokenize_tags(i2b2_xml)
    tokens = FeatureServiceClient().annotate(get_text(i2b2_xml))
    # text now is a list of token dict

    # TODO: dynamic programming for speed boost
    # add phi tag to the token if the phi type of this token is already known
    for phi in tags:
        for i in range(len(tokens)):
            if overlap_ranges(phi, tokens[i]['range']):
                # print('**************')
                # print(phi)
                # print(tags[phi])
                # print(text[i]['token'])
                tokens[i]['phi'] = tags[phi]['phi']
    return tokens


###############################################################################
#
# Get and process samples: training/testing
#
###############################################################################

def get_training_files(file_type='.txt'):
    train_files = common.get_file_list(TRAIN_DIR, file_type)
    for i in range(len(train_files)):
        train_files[i] = (train_files[i][:-4] + '.surrogate_phi.json')
    return train_files


def get_training_files_to_populate(file_type='.txt'):
    train_files = common.get_file_list(TRAIN_DIR, file_type)
    return train_files


def get_testing_files(file_type='.txt'):
    test_files = common.get_file_list(TRAIN_DIR, file_type)
    for i in range(len(test_files)):
        test_files[i] = (test_files[i][:-4] + '.surrogate_phi.json')
    return test_files


###############################################################################
#
# Get and process samples: training/testing
#
###############################################################################

def populate_phi_types():
    """
    populate each token in the featureset json file with the phi type in the .json file
    :return:
    """
    # This algorithm doesn't work, may change to go through every single phi token,

    files = get_training_files_to_populate('.txt')
    flag = False
    for file in files:
        result = list()
        file_to_populate = file[:-4] + '.featureset.annotate_text.json'
        file_with_suggestion = file[:-4] + '.json'
        tokens = common.read_json(file_to_populate)
        phis = common.read_json(file_with_suggestion)
        i = 0  # index the phi list
        j = 0  # index the token list
        while i < len(phis):
            phi = phis[i]
            i += 1
            while j < len(tokens):
                token = tokens[j]
                if (token['token'] not in string.punctuation) and (
                        list(phi.values())[0] in token['token'] or token['token'] in list(phi.values())[0]):
                    token['phi'] = list(phi.keys())[0]
                    result.append(token)
                    j += 1
                    flag = True
                    continue  # continue with the inner loop to get the next token
                else:
                    if flag:
                        # if last one is found as phi but this one doesn't match, should try move phi forward to check
                        # before say this is not a phi
                        flag = False
                        break
                    else:
                        result.append(token)
                        j += 1
                        continue

        file_with_phi = (file[:-4] + '.surrogate_phi.json')
        result = {'file': file, 'tokenize': result}
        common.write_json(result, file_with_phi)


def populate_phi_with_range():
    files = get_training_files_to_populate('.txt')
    flag = False
    for file in files:

        result = list()
        file_to_populate = file[:-4] + '.featureset.annotate_text.json'
        file_with_suggestion = file[:-4] + '.json'
        tokens = common.read_json(file_to_populate)
        phis = common.read_json(file_with_suggestion)
        i = 0  # index of the token list
        j = 0  # index of the phi list
        # TODO: exclude punctuation as phi or not
        while i < len(phis):
            phi = phis[i]
            i += 1
            while j < len(tokens):
                token = tokens[j]
                if overlap_ranges(phi['range'], token['range']):
                    if token['token'] in string.punctuation:
                        result.append(token)
                        j += 1
                        continue  # if this token is a punctuation phi, then move on to the next token
                    else:
                        token['phi'] = list(phi.keys())[0]
                        result.append(token)
                        j += 1
                        flag = True
                        continue
                else:
                    if flag:
                        flag = False
                        break
                    else:
                        result.append(token)
                        j += 1
                        continue
        file_with_phi = (file[:-4] + '.surrogate_phi.json')
        result = {'file': file, 'tokenize': result}
        common.write_json(result, file_with_phi)
