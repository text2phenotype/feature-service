"""
Old aspect dataset parser
@author: Richen
Aspect: sample from I2b2 2009 medication challenge
JIRA/BIOMED-235
"""
# -*- coding: UTF-8 -*-
# import numpy
# from sklearn.feature_extraction.text import CountVectorizer
import re
import string
import os
from pathlib import Path

# from tokenizer import Tokenizer
import glob
import operator
import csv
import json


def create_mapping(file_map):
    """
    :param file_map: string, the filepath of the mappings
    :return: dictionary with key - section heading, value the corresponding aspect
    """
    if os.path.exists(file_map):
        with open(file_map) as data_file:
            print(file_map)
            result = json.load(data_file)
    return result


def parse(filepath):
    """This function takes in a filepath and populate two lists: train_text and train_labels
    train_labels stores the headings and train_text stores the train_text of the corresponding headings
    :param: filepath - the path to that .txt file
    :return: a list of train_text and a list of train_labels of this file
    """
    train_text = []  # a list of text chunk under each section
    train_labels = []  # a list of section heading in the file
    with open(filepath, "r") as f:
        lines = f.readlines()
        text_chunk = ""
        for line in lines:
            line = line.strip()
            # TODO: this part needs to be modified to extract more heading because of the format such as "Feeds at discharge : Enfamil 20 p.o. ad lib .""

            # borrow code FROM BIOMED 22
            # if : is in the middle of the line, take the first part before ':' as the section heading and the text after that as the content
            # this if statement was newly written and hasn't been tested yet, need to test. The idea was to cope with the line where ':' is in the middle

            if ":" in line:
                section = line.split(":")[0].strip()
                # Remove the punctuation and digits of the text
                section = "".join(
                    c for c in section if c not in string.punctuation and not c.isdigit()
                ).strip()
                train_labels.append(section.upper())
                train_text.append(text_chunk)
                text_chunk = line.split(":")[1].strip()

            # if the line ends with ':'
            if line.endswith(":"):
                section = "".join(
                    c for c in line if c not in string.punctuation and not c.isdigit()
                ).strip()
                train_labels.append(section.upper())
                train_text.append(text_chunk)
                text_chunk = ""
            else:
                # build a long string until next section heading
                text_chunk += " " + line
    # append the last piece of text
    train_text.append(text_chunk)
    train_text.pop(0)
    # print train_labels
    # for i in range(len(train_labels)):
    # 	print 'the section heading is:' + train_labels[i]
    # 	print 'the text is:' + train_text[i]
    # print (train_labels)
    if len(train_labels) != len(train_text):
        print("length not match error!")
        return False
    # TO DO:
    # also when we return, we should strip out the number in front of the string. in train_labels
    return train_text, train_labels


def create_examples(train_text, train_labels):
    """
    TODO, not yet finished
    create examples for CRF/Bi RNN model from all .txt file in Examples Folder, write them to a .txt file
    :param train_text:
    :param train_labels:
    :return:
    """
    left_out_sections = {}
    fileDir = os.path.dirname(os.path.realpath("__file__"))
    path_pre = "/Section_Classification_I2B2/"
    section_aspect_map = create_mapping("section_aspect_mapping.json")
    with open("new_file.csv") as file_train:
        csvwriter = csv.writer(file_train)
        for root, dirs, files in os.walk(path_post):
            for file in files:
                # find a file name that ends with .txt, parse it and then write it to file.
                if file.endswith(".txt"):
                    path_full = path_pre + os.path.join(root, file)
                    filepath = str(Path(fileDir).parent) + path_full
                    train_text, train_labels = parse(filepath)
                    csvwriter.writerow(train_labels, train_text)


def write_to_files(train_text, train_labels):
    """
    write to CSV files of the training data and training labels to store.
    """
    # fields = ['section_label', 'string'] #0 for lab, 1 for medication
    with open("train.csv", "w") as f_train:
        csvwriter = csv.writer(f_train)
        # csvwriter.writerow(fields)
        # print "Hello"
        for i in range(len(train_text)):
            csvwriter.writerow([train_labels[i], train_text[i]])


def create_data_file(path_post, flag=False):
    """
    create training datafile from .txt file in Examples Folder, finding all .txt files and write section
    headings and text to a .csv file.
    :param: path_post - string, the root directory that contains all the example files
    labeling: refer to the aspect_list
    """
    aspect_list = [
        "allergy",
        "immunization",
        "lab",
        "medication",
        "procedure",
        "diagnosis",
        "problem",
        "demographics",
        "encounter",
        "physical_exam",
        "treatment",
        "social",
        "device",
        "other",
    ]
    left_out_sections = {}
    fileDir = os.path.dirname(os.path.realpath("__file__"))
    path_pre = "/Section_Classification_I2B2/"
    section_aspect_map = create_mapping("section_aspect_mapping.json")
    # print (len(section_aspect_map))
    with open("medication_challenge_12_class.bsv", "w") as file_train:
        # create '|' delimited file.
        csvwriter = csv.writer(file_train, delimiter="|")
        for root, dirs, files in os.walk(path_post):
            for file in files:
                # for medication challenge, if '.' not in that file, then it's discharge file in medication challenge
                if "." not in file:
                    # compose the full path of this .txt file.
                    path_full = path_pre + os.path.join(root, file)
                    filepath = str(Path(fileDir).parent) + path_full
                    print(filepath)

                    if parse(filepath) != False:
                        train_text, train_labels = parse(filepath)
                        # print (train_labels)
                        for i in range(len(train_labels)):
                            # if train_labels[i].upper() not in section_list:
                            # 	section_list.append(train_labels[i].upper())
                            # Idea: we write medication to the file, if medication is in the aspect of the section_heading that matches the current heading
                            # or "MEDICATION" is in the string, same for other aspect
                            if train_labels[i] in section_aspect_map:
                                # get the index of the aspect in the aspect list
                                label = aspect_list.index(section_aspect_map[train_labels[i]][7:])
                                if label != 13 and label != 12:
                                    if not flag:
                                        csvwriter.writerow(
                                            [
                                                int(
                                                    aspect_list.index(
                                                        section_aspect_map[train_labels[i]][7:]
                                                    )
                                                ),
                                                str(train_text[i]),
                                            ]
                                        )
                                    else:
                                        csvwriter.writerow(
                                            [
                                                int(
                                                    aspect_list.index(
                                                        section_aspect_map[train_labels[i]][7:]
                                                    )
                                                ),
                                                str(train_labels[i] + " " + train_text[i]),
                                            ]
                                        )
                            elif "MEDICATION" in train_labels[i]:
                                print(train_labels[i])
                                if train_text[i]:
                                    csvwriter.writerow([3, str(train_text[i])])
                                print("Unknown potential header found!")
                                if train_labels[i] not in left_out_sections:
                                    left_out_sections[train_labels[i]] = 1
                                else:
                                    left_out_sections[train_labels[i]] += 1
                            else:
                                print("Unknown potential header found!")
                                if train_labels[i] not in left_out_sections:
                                    left_out_sections[train_labels[i]] = 1
                                else:
                                    left_out_sections[train_labels[i]] += 1
                            # elif "other" in section_aspect_map[train_labels[i]] and train_text[i]:
                            # 	csvwriter.writerow([5, train_text[i]])
                    """
						elif "MEDICATION" in train_labels[i]:
							if train_text[i]:
								csvwriter.writerow([0, train_text[i]])
						elif "PROCEDURE" in train_labels[i]:
							if train_text[i]: 
								csvwriter.writerow([1, train_text[i]])
						elif "ALLERGY" in train_labels[i]:
							if train_text[i]:
								csvwriter.writerow([2, train_text[i]])
						elif "LAB" in train_labels[i]:
							if train_text[i]:
								csvwriter.writerow([3, train_text[i]])
						elif "PROBLEM" in train_labels[i]:
							if train_text[i]:
								csvwriter.writerow([4, train_text[i]])
						elif "DIAGNOSIS" in train_labels[i] or "DIAGNOSES" in train_labels[i]:
							if train_text[i]:
								csvwriter.writerow([4, train_text[i]])
						else:
							if train_labels[i] not in left_out_sections:
								left_out_sections[train_labels[i]] = 1
							else:
								left_out_sections[train_labels[i]] += 1
						"""

    # left_out_section_sorted = dict(sorted(left_out_sections.items(), key=operator.itemgetter(1), reverse = True))
    # js = json.dumps(left_out_section_sorted)
    # with open('unknown_potential_left_out_header.json', 'w') as fp:
    # 	fp.write(js)
    # check if a substring is in a string


def create_sequential_examples(path_post):
    """
    create sequential examples from all .txt files in the examples folder
    :param path_post - string, the path of the directory that contains the example files.

    :return: None
    """
    # Find all the files in the Example folder and populate a bsv file with a list of sectoin headings and a list of content.
    # Make use of the parse function
    fileDir = os.path.dirname(os.path.realpath("__file__"))
    path_pre = "/Section_Classification_I2B2/"
    section_aspect_map = create_mapping("section_aspect_mapping.json")
    aspect_list = [
        "allergy",
        "immunization",
        "lab",
        "medication",
        "procedure",
        "diagnosis",
        "problem",
        "demographics",
        "encounter",
        "physical_exam",
        "treatment",
        "social",
        "device",
        "other",
    ]
    with open("sequential_examples.bsv", "rb") as file_train:
        csvwriter = csv.writer(file_train, delimiter="|")
        for root, dirs, files in os.walk(path_post):
            for file in files:
                if file.endswith(".txt"):
                    # compose the full path of this .txt file.
                    path_full = path_pre + os.path.join(root, file)
                    filepath = str(Path(fileDir).parent) + path_full
                    if parse(filepath) != False:
                        train_text, train_labels = parse(filepath)


def find_all_sections(path_post):
    """
    This function returns all possible section headings of the folder_path
    path is the directory path that was
    :param: path_post is the directory path that contains all examples
    """
    section_set = set()
    section_dict = {}
    fileDir = os.path.dirname(os.path.realpath("__file__"))
    path_pre = "/Section_Classification_I2B2/"
    counter = 0
    for root, dirs, files in os.walk(path_post):
        for file in files:
            # find all files in Example directory that has the ending .txt
            if file.endswith(".txt"):
                counter += 1
                path_full = path_pre + os.path.join(root, file)
                filepath = str(Path(fileDir).parent) + path_full
                _, train_labels = parse(filepath)
                for label in train_labels:
                    if label not in section_set:
                        section_set.add(label)
                    if label in section_dict:
                        section_dict[label] += 1
                    else:
                        section_dict[label] = 1
    section_dict = sorted(section_dict.items(), key=operator.itemgetter(1), reverse=True)
    # print counter
    return section_dict


if __name__ == "__main__":
    # rel_path = "/Section_Classification_I2B2/Examples/Beth_Train/clinical-33.txt"
    # fileDir = os.path.dirname(os.path.realpath('__file__'))
    # filepath = str(Path(fileDir).parent) + rel_path
    create_data_file("Examples/2009 Medication Challenge/", False)
    # print (parse('/Users/richen.zhang/Documents/Section_Classification_I2B2/Examples/2009 Medication Challenge/training.sets.released/9/976556'))
    # train_text, train_labels = parse(filepath)
    # print train_labels
    # write_to_files(train_text, train_labels)
    # find_all_sections("Examples/")
