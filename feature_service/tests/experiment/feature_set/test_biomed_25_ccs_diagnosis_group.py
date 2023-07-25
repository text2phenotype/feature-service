import os, csv
import unittest

from text2phenotype.common.log import operations_logger

from feature_service.feature_service_env import FeatureServiceEnv

# from biomed.db.sql import db

CCS_DIR = os.path.join(FeatureServiceEnv.DATA_ROOT.value, 'biomed', 'featureset', 'ccs')

ICD9_DX = 'ccs_multi_dx_tool_2015.csv'
ICD9_PR = 'ccs_multi_pr_tool_2015.csv'
ICD10_DX = 'ccs_dx_icd10cm_2017.csv'
ICD10_PR = 'ccs_pr_icd10pcs_2017.csv'

ICD9_DX_LABEL = 'dxmlabel-13.csv'
ICD9_PR_LABEL = 'prmlabel-09.csv'
ICD10_DX_LABEL = 'dxmlabel10.csv'
ICD10_PR_LABEL = 'prmlabel10.csv'


###############################################################################
#
# Read CSV
#
###############################################################################
def read_csv_labels(csvfile):
    """
    Get dict of human readable labels for CCS
    :param csvfile: Clinical Classification System file https://www.hcup-us.ahrq.gov/toolssoftware/ccs/ccs.jsp
    :return:
    """
    keyvals = dict()

    with open(csvfile, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        next(csvreader, None)  # skip the headers
        for row in csvreader:
            level = row[0].strip()
            label = row[1].strip()

            keyvals[level] = label
    return keyvals


def read_csv_tree_icd9(csvfile=ICD9_DX):
    """
    :param csvfile: read ccs_multi_**_tool**.csv file and get a dictionary of the content
    :return: dict where key= ICD9 and val=metadata
    """
    keyvals = dict()

    with open(csvfile, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='\"')

        next(csvreader, None)  # skip the headers

        for row in csvreader:
            code = clean(row[0])

            keyvals[code] = {
                'L1': clean(row[1]),
                'L1_label': clean(row[2]),
                'L2': clean(row[3]),
                'L2_label': clean(row[4]),
                'L3': clean(row[5]),
                'L3_label': clean(row[6]),
                'L4': clean(row[7]),
                'L4_label': clean(row[8]),
                'code': code,
                'label': ''}

    return keyvals


def read_csv_tree_icd10(csvfile=ICD10_DX):
    """
    :param csvfile: read ccs_multi_**_tool**.csv file and get a dictionary of the content
    :return: dict where key= ICD10 and val=metadata
    """
    keyvals = dict()

    with open(csvfile, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='\"')

        next(csvreader, None)  # skip the headers

        for row in csvreader:
            code = clean(row[0])

            keyvals[code] = {
                'L1': clean(row[1]),
                'L1_label': clean(row[3]),
                'L2': clean(row[4]),
                'L2_label': clean(row[5]),
                'L3': clean(row[6]),
                'L3_label': clean(row[7]),
                'L4': '',
                'L4_label': '',
                'code': code,
                'label': clean(row[2])}

    return keyvals


def clean(column: str):
    """
    :param column: raw data from CCS download
    :return: cleaned string
    """
    return column.strip().replace('\"', '').replace('\'', '')


###############################################################################
#
# Insert into DB
#
###############################################################################
def insert_ccs_tree(entry, vocab='ICD9'):
    """
    Insert ccs_tree into DEID database
    """
    e = entry

    insert = f" INSERT into ccs_tree (code,L1,L1_label,L2,L2_label,L3,L3_label,L4,L4_label,label,vocab) values "
    insert += f" VALUES ('{e['code']}','{e['L1']}','{e['L1_label']}','{e['L2']}','{e['L2_label']}','{e['L3']}','{e['L3_label']}','{e['L4']}','{e['L4_label']}','{e['label']}', {vocab})"

    operations_logger.debug(insert)

    return db.query(insert)


###############################################################################
#
# Get CCS data for ICD code
#
###############################################################################

def get_hierarchy_for_code(vocab, icd_code):
    """
    Get hierarchical paths for a given code

    :param vocab: str like 'icd9'
    :param icd_code: '410.9' or '4109'
    :return: ordered list of hierarchical 'paths' to code, like

    '7',"Diseases of the circulatory system",
    '7.1',"Hypertension",
    '7.1.1',"Essential hypertension"
    """
    raise Exception('NOT YET IMPLEMENTED')


class TestBiomed25(unittest.TestCase):

    def test_csv_labels_feature_dimension(self):
        labels = read_csv_labels(os.path.join(CCS_DIR, 'ICD9', ICD9_DX_LABEL))
        self.assertEquals(729, len(labels))

        labels = read_csv_labels(os.path.join(CCS_DIR, 'ICD9', ICD9_PR_LABEL))
        self.assertEquals(405, len(labels))

        labels = read_csv_labels(os.path.join(CCS_DIR, 'ICD10', ICD10_DX_LABEL))
        self.assertEquals(153, len(labels))

        labels = read_csv_labels(os.path.join(CCS_DIR, 'ICD10', ICD10_PR_LABEL))
        self.assertEquals(222, len(labels))
