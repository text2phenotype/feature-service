from operator import itemgetter
import os

from text2phenotype.apiclients.feature_service import FeatureServiceClient
from text2phenotype.common import common
from text2phenotype.common.feature_data_parsing import overlap_ranges
from text2phenotype.common.log import operations_logger

from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.nlp import autocode


I2B2_2009_DIR = os.path.join(FeatureServiceEnv.DATA_ROOT.value, 'I2B2', '2009 Medication Challenge')

GROUND_TRUTH_DIR = os.path.join(I2B2_2009_DIR, 'training.ground.truth')

TRAIN_TEST_DIR = os.path.join(I2B2_2009_DIR, 'train.test.released.8.17.09')

TRAIN_DIR = os.path.join(I2B2_2009_DIR, 'training.sets.released')

ANNOTATION_DIR = os.path.join(I2B2_2009_DIR, 'annotations.1.11.09', 'converted.noduplicates.sorted')

ANNOTATION_GOLD_DIR = os.path.join(I2B2_2009_DIR, 'gold')

GOLD_RAW_TXT_DIR = os.path.join(ANNOTATION_GOLD_DIR, 'gold_raw_text')

ANNOTATION_GOLD_TRAIN_DIR = os.path.join(ANNOTATION_GOLD_DIR, 'Aug_3_5PM', 'train')

ANNOTATION_GOLD_TEST_DIR = os.path.join(ANNOTATION_GOLD_DIR, 'Aug_3_5PM', 'test')

EXPERT_LABEL_DIR = os.path.join(ANNOTATION_GOLD_DIR, 'expert_label')

DRUG_NER_DIR = os.path.join(TRAIN_TEST_DIR, 'drug_ner_richen.zhang_2018-05-21_1526968446.92793')

TEXT2SUMMARY_DIR = os.path.join(TRAIN_TEST_DIR, 'text2summary_richen.zhang_2018-05-21_1526968446.881067')


def annotate_training_files_with_drug_ner(file_dir):
    """
    This function takes all the files in the train_test folder and annotate the file
    with autocode.drug_ner or pref_terms.
    :return:
    """
    file_list = common.get_file_list(file_dir, '')
    text2summary_ver_dir = os.path.join(file_dir, common.version_text('text2summary'))
    if not os.path.exists(text2summary_ver_dir):
        os.mkdir(text2summary_ver_dir)

    drug_ner_ver_dir = os.path.join(file_dir, common.version_text('drug_ner'))
    if not os.path.exists(drug_ner_ver_dir):
        os.mkdir(drug_ner_ver_dir)

    for file in file_list:
        text = common.read_text(file)
        summary_annotation = pref_terms.text_to_summary(text)

        common.write_json(summary_annotation, os.path.join(text2summary_ver_dir, f"{str(file.split('/')[-1])}.json"))
        drug_annotation = autocode.drug_ner(text)
        # TODO: can also annotate with drug_ner in autocode
        common.write_json(drug_annotation, os.path.join(drug_ner_ver_dir, f"{str(file.split('/')[-1])}.json"))


def calculate_statistics():
    """
    This function takes the result from drug_ner or text2summary and annotations and get precision recall
    for the drug_ner
    :return: precision/recall for medication
    """
    # steps:
    # 1. parse the file that contains the annotation either in annotation_dir or ground_truth_dir
    # try to figure out the range based on start end index, as the range is best for matching
    # 2. find if this term is caught in drug_ner match the same record with id number of that record

    annotation_file_list = common.get_file_list(ANNOTATION_DIR, '.m')
    annotation_file_list.extend(common.get_file_list(GROUND_TRUTH_DIR, '.entries'))

    annotation_dir = os.path.join(ANNOTATION_GOLD_DIR, common.version_text('human_expert'))

    if not os.path.exists(annotation_dir):
        os.mkdir(annotation_dir)

    operations_logger.info(f'total number of files to analyze: {str(len(annotation_file_list))}')

    TP_tot_recall = 0
    FP_tot = 0
    TN_tot = 0
    FN_tot = 0
    TP_tot_precision = 0
    FN_tot_dict = dict()
    FP_tot_dict = dict()

    for file in annotation_file_list:
        TP_recall = 0
        FP = 0
        TN = 0
        FN = 0
        TP_precision = 0
        FP_list = list()
        FN_list = list()
        ground_truth = list()  # this list contains ground truth medication list of this record record_id

        if file[-1] == 'm':
            file_id = file.split('/')[-1].split('.')[0]
        else:
            file_id = file.split('/')[-1].split('_')[0]

        original_file = os.path.join(TRAIN_TEST_DIR, file_id)

        # TODO: some txt file is not annotated through drug_ner, about 200 left, what if this file doesn't exist?

        drug_ner_file = os.path.join(DRUG_NER_DIR, str(file_id) + '.json')

        text = common.read_text(original_file)

        annotation = common.read_text(file)

        for line in annotation.split('\n'):
            if line:
                medication = line.split('||')[0].split('"')[1]
                # TODO: find range here and append that to medication term
                med_range = find_range(text, line)
                start = min(med_range)
                end = max(med_range) + 1
                ground_truth.append({'annotated_med': medication, 'range': [start, end]})

        # sort the dictionary by the start index of the annotation refer to this:
        # https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python
        # ground_truth = sorted(ground_truth, key = itemgetter('range'))

        # common.write_json(ground_truth, os.path.join(annotation_dir, f"{file_id}.json"))
        # common.write_text(text, os.path.join(annotation_dir, f"{file_id}.txt"))

        # TODO: include polarity when deciding whether this is a prediction or not. if negative, then not
        # TODO: once an allergy (should make use of chunker here), always an allergy, some drug ner
        # TODO: extraction are allergy-wise medication terms

        prediction = list()
        drug_ner_json = common.read_json(drug_ner_file)
        drug_list = drug_ner_json['drugEntities']
        for drug in drug_list:
            # exclude the negative mention
            if drug['attributes']['polarity'] != 'negative':
                prediction.append(
                    {'predicted_med': drug['text'][0].lower(), 'range': [drug['text'][1], drug['text'][2]]})

        prediction = sorted(prediction, key=itemgetter('range'))

        flag = False
        # print (prediction)
        for truth in ground_truth:
            for pred in prediction:
                if overlap_ranges(truth['range'], pred['range']):
                    TP_recall += 1
                    flag = True
                    break
            if not flag:
                if truth['annotated_med'] not in FN_tot_dict:
                    FN_tot_dict[truth['annotated_med']] = [0, []]
                FN_tot_dict[truth['annotated_med']][0] += 1
                FN_tot_dict[truth['annotated_med']][1].append(file_id)
            flag = False

        # Equation: TP + FN = len(ground_truth)
        # Equation: TP + FP = len(prediction)
        FN = len(ground_truth) - TP_recall
        TP_tot_recall += TP_recall
        FN_tot += FN
        FP_list = list()

        flag = False
        for pred in prediction:
            for truth in ground_truth:
                if overlap_ranges(truth['range'], pred['range']):
                    TP_precision += 1
                    flag = True
                    break
            if not flag:
                if pred['predicted_med'] not in FP_tot_dict:
                    FP_tot_dict[pred['predicted_med']] = [0, []]
                FP_tot_dict[pred['predicted_med']][0] += 1
                FP_tot_dict[pred['predicted_med']][1].append(file_id)
            flag = False

        FP = len(prediction) - TP_precision
        FP_tot += FP
        TP_tot_precision += TP_precision

    recall = float(TP_tot_recall / (TP_tot_recall + FN_tot))
    precision = float(TP_tot_precision / (TP_tot_precision + FP_tot))

    # FP_tot_dict = OrderedDict(sorted(FP_tot_dict.items(), key = itemgetter(1), reverse = True))
    common.write_json(FP_tot_dict, os.path.join(GROUND_TRUTH_DIR, f"{common.version_text('FP_ID')}.json"))

    # FN_tot_dict = OrderedDict(sorted(FN_tot_dict.items(), key = itemgetter(1), reverse = True))
    common.write_json(FN_tot_dict, os.path.join(GROUND_TRUTH_DIR, f"{common.version_text('FN_ID')}.json"))

    return precision, recall


def calculate_statistics_with_cui():
    """
    This function takes the result from drug_ner or text2summary and annotations and get precision recall
    for the drug_ner
    :return: precision/recall for medication
    """
    # steps: 1. parse the file that contains the annotation either in annotation_dir or ground_truth_dir
    #          try to figure out the range based on start end index, as the range is best for matching
    #       2. find if this term is caught in drug_ner
    #       match the same record with id number of that record

    annotation_file_list = common.get_file_list(ANNOTATION_DIR, '.m')
    annotation_file_list.extend(common.get_file_list(GROUND_TRUTH_DIR, '.entries'))

    '''
    annotation_dir = os.path.join(ANNOTATION_GOLD_DIR, version.version_text('human_expert'))

    if not os.path.exists(annotation_dir):
        os.mkdir(annotation_dir)
    '''

    operations_logger.info(f'total number of files to analyze: {str(len(annotation_file_list))}')

    TP_tot_recall = 0
    FP_tot = 0
    TN_tot = 0
    FN_tot = 0
    TP_tot_precision = 0
    FN_tot_dict = dict()
    FP_tot_dict = dict()

    for file in annotation_file_list:
        TP_recall = 0
        FP = 0
        TN = 0
        FN = 0
        TP_precision = 0
        FP_list = list()
        FN_list = list()
        ground_truth = list()  # this list contains ground truth medication list of this record record_id

        if file[-1] == 'm':
            file_id = file.split('/')[-1].split('.')[0]
        else:
            file_id = file.split('/')[-1].split('_')[0]

        original_file = os.path.join(TRAIN_TEST_DIR, file_id)

        # TODO: some txt file is not annotated through drug_ner, about 200 left, what if this file doesn't exist?

        drug_ner_file = os.path.join(DRUG_NER_DIR, str(file_id) + '.json')

        text = common.read_text(original_file)

        annotation = common.read_text(file)

        for line in annotation.split('\n'):
            if line:
                medication = line.split('||')[0].split('"')[1]
                # TODO: find range here and append that to medication term
                med_range = find_range(text, line)
                start = min(med_range)
                end = max(med_range) + 1
                ground_truth.append({'annotated_med': medication, 'range': [start, end]})

        # sort the dictionary by the start index of the annotation
        # refer to this: https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python
        ground_truth = sorted(ground_truth, key=itemgetter('range'))

        # common.write_json(ground_truth, os.path.join(annotation_dir, f"{file_id}.json"))
        # common.write_text(text, os.path.join(annotation_dir, f"{file_id}.txt"))

        # TODO: include polarity when deciding whether this is a prediction or not. if negative, then not
        # TODO: once an allergy (should make use of chunker here), always an allergy, some drug ner
        # TODO: extraction are allergy-wise medication terms

        prediction = list()
        drug_ner_json = common.read_json(drug_ner_file)
        drug_list = drug_ner_json['drugEntities']
        for drug in drug_list:
            # exclude the negative mention
            if drug['attributes']['polarity'] != 'negative':
                prediction.append(
                    {'predicted_med': drug['text'][0].lower(), 'range': [drug['text'][1], drug['text'][2]],
                     'umlsConcept': drug['umlsConcept']})

        prediction = sorted(prediction, key=itemgetter('range'))

        flag = False
        # print (prediction)
        for truth in ground_truth:
            for pred in prediction:
                if overlap_ranges(truth['range'], pred['range']):
                    TP_recall += 1
                    flag = True
                    break
            if not flag:
                if truth['annotated_med'] not in FN_tot_dict:
                    FN_tot_dict[truth['annotated_med']] = [0, []]
                FN_tot_dict[truth['annotated_med']][0] += 1
                FN_tot_dict[truth['annotated_med']][1].append(file_id)
            flag = False

        # Equation: TP + FN = len(ground_truth)
        # Equation: TP + FP = len(prediction)
        FN = len(ground_truth) - TP_recall
        TP_tot_recall += TP_recall
        FN_tot += FN
        FP_list = list()

        flag = False
        for pred in prediction:
            for truth in ground_truth:
                if overlap_ranges(truth['range'], pred['range']):
                    TP_precision += 1
                    flag = True
                    break
            if not flag:
                if pred['predicted_med'] not in FP_tot_dict:
                    FP_tot_dict[pred['predicted_med']] = [0, [], []]
                FP_tot_dict[pred['predicted_med']][0] += 1
                FP_tot_dict[pred['predicted_med']][1].append(file_id)
                FP_tot_dict[pred['predicted_med']][2].extend(pred['umlsConcept'])
            flag = False

        FP = len(prediction) - TP_precision
        FP_tot += FP
        TP_tot_precision += TP_precision

    recall = float(TP_tot_recall / (TP_tot_recall + FN_tot))
    precision = float(TP_tot_precision / (TP_tot_precision + FP_tot))

    # FP_tot_dict = OrderedDict(sorted(FP_tot_dict.items(), key = itemgetter(1), reverse = True))
    common.write_json(FP_tot_dict, os.path.join(GROUND_TRUTH_DIR, f"{common.version_text('FP_cui')}.json"))

    # FN_tot_dict = OrderedDict(sorted(FN_tot_dict.items(), key = itemgetter(1), reverse = True))
    common.write_json(FN_tot_dict, os.path.join(GROUND_TRUTH_DIR, f"{common.version_text('FN_cui')}.json"))

    return precision, recall


# need to be tested
def find_range(text, line):
    """
    this takes in the original text and a line in annotation files
    return the range of the medication of the annotation in the original text
    :param text: clinical text
    :param line: a line in the annotation file
    :return:
    """
    # get the start/end position of the annotation
    offset = line.split('||')[0].split('"')[2]
    offset_list = offset.split()
    start_line_num = int(offset_list[0].split(':')[0].strip())
    start_token_num = int(offset_list[0].split(':')[1].strip())
    end_line_num = int(offset_list[-1].split(':')[0].strip())
    end_token_num = int(offset_list[-1].split(':')[1].strip())

    line_list = text.split('\n')
    # what if the token is the first one
    start_index = len('\n'.join(line_list[:start_line_num - 1])) + 1 + len(
        ' '.join(line_list[start_line_num - 1].split()[:start_token_num]))

    if start_token_num != 0:
        start_index += 1

    end_index = len('\n'.join(line_list[:end_line_num - 1])) + 1 + len(
        ' '.join(line_list[end_line_num - 1].split()[:end_token_num]))

    if end_token_num != 0:
        end_index += 1

    end_index += len(line_list[end_line_num - 1].split()[end_token_num])

    return range(start_index, end_index)


def annotate_training_files_with_featureset(file_dir):
    """
    annotate all the txt files in the dir with featureset annotation and write annotation json to the same directory
    :param file_dir: the directory that contains txt files to annotate
    :return:
    """
    feature_service_client = FeatureServiceClient()
    file_list = common.get_file_list(file_dir, '.txt')
    for file in file_list:
        text = common.read_text(file)
        tokens = feature_service_client.annotate(text)
        file_to_write = file[:-4] + '.featureset.annotate_text.json'
        common.write_json(tokens, file_to_write)
