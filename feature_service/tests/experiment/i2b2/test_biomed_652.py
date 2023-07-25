import unittest
import os
import string
from collections import defaultdict
from typing import List, Dict, Set

from text2phenotype.common import common
from text2phenotype.common.log import operations_logger
from text2phenotype.entity.brat import BratReader
from text2phenotype.annotations.file_helpers import Annotation

from feature_service.tests.experiment.i2b2 import i2b2_2014
from feature_service.feature_service_env import FeatureServiceEnv


class TestBiomed652(unittest.TestCase):
    READER = BratReader()
    
    def test_to_brat(self):
        # TODO: talk to adam about best practice for pulling samples
        SAMPLE_ROOT_DIR = os.path.join(FeatureServiceEnv.DATA_ROOT.value, 'I2B2',
                                       '2014 De-identification and Heart Disease Risk Factors Challenge')
        HDRF_ROOT_DIR = os.path.join(SAMPLE_ROOT_DIR, 'HeartRisk')
        HDRF_SAMPLE_DIRS = [os.path.join(HDRF_ROOT_DIR, d) for d in 
                       ['testing-RiskFactors-Complete', 
                        'training-RiskFactors-Complete-Set1', 
                        'training-RiskFactors-Complete-Set2']]
        
        skipped_count = 0
        for sample_dir in HDRF_SAMPLE_DIRS:
            sample_files = common.get_file_list(sample_dir, 'xml')
            
            versioned_dir = os.path.join(sample_dir, common.version_text('surrogates'))
            if not os.path.exists(versioned_dir):
                os.mkdir(versioned_dir)
            
            operations_logger.info(f"Processing {len(sample_files)} records from {sample_dir}...")
            skipped_count += self.__process_sample_files(sample_files, versioned_dir)
        
        operations_logger.info(f"Skipped writing outputs for a total of {skipped_count} files.")
    
    def __process_sample_files(self, files: List[str], output_dir: str):
        FILE_COUNT = len(files)
        
        record_count = 0
        skipped_count = 0
        for sample_files in self.__group_samples(files).values():
            skipped_count += self.__process_sample_group(sample_files, output_dir)
            
            operations_logger.info(f"Completed: {record_count+1}-{record_count+len(sample_files)} of {FILE_COUNT}")
            record_count += len(sample_files)

        return skipped_count

    @staticmethod
    def __group_samples(sample_files: List[str]) -> Dict[str, Set[str]]:
        groups = defaultdict(set)
        
        for sample_file in sorted(sample_files):
            groups[os.path.basename(sample_file).split('-')[0]].add(sample_file)
        
        return groups

    @staticmethod
    def __text_equal(t1: str, t2: str) -> bool:
        trans = str.maketrans('', '', string.whitespace + string.punctuation)
        
        return t1.translate(trans) == t2.translate(trans)

    @staticmethod
    def __make_annotation(child_node) -> Annotation:
        orig_start = int(child_node.attrib['start'])
        orig_text = child_node.attrib['text']
        
        annotation = Annotation({'aspect': child_node.tag})
        annotation.text = orig_text.lstrip().lstrip(string.punctuation)
        start = orig_start + len(orig_text) - len(annotation.text)
        
        annotation.text = annotation.text.rstrip().rstrip(string.punctuation)
        annotation.spans = ((start, start + len(annotation.text)),)
        
        return annotation
    
    def __process_sample_group(self, sample_files: List[str], output_dir: str) -> int:
        file_error_count = 0
        
        for sample_file in sample_files:
            operations_logger.info(f"Processing file {sample_file}...")
            
            record_text = i2b2_2014.get_text(sample_file)
            record_tags = i2b2_2014.get_raw_tags(sample_file)

            has_bad_annotation = False
            annotations = list()
            for record_tag in record_tags:
                if record_tag.tag == 'PHI':
                    continue
                
                if record_tag.tag == 'SMOKER' and record_tag.attrib['status'] == 'unknown':
                    continue
                
                if record_tag.tag == 'FAMILY_HIST' and record_tag.attrib['indicator'] == 'not present':
                    continue
                
                for _child in record_tag.getchildren():
                    if 'text' not in _child.attrib:
                        continue
                    
                    if len(_child.attrib['text']) != int(_child.attrib['end']) - int(_child.attrib['start']):
                        actual_text = record_text[int(_child.attrib['start']):int(_child.attrib['end'])]
                        if '&gt;' in _child.attrib['text'] and '&gt;' not in actual_text:
                            _child.attrib['text'] = actual_text
                        else:
                            has_bad_annotation = True
                            file_error_count += 1
                            break
                    
                    annotation = self.__make_annotation(_child)
                    
                    span = annotation.spans[0]
                    actual_text = record_text[span[0]:span[1]]
                    if not self.__text_equal(actual_text, annotation.text):
                        raise Exception(f"'{actual_text}' != '{annotation.text}'")
                    
                    annotations.append(annotation)
                
                if has_bad_annotation:
                    break
                
            if has_bad_annotation:
                operations_logger.warning("Found bad annotations. Skipping outputs.")
                continue
            
            self.READER.annotations.clear()
            for annotation in self.__resolve_overlapping_annotations(annotations):
                self.READER.add_annotation(annotation)
            
            file_base = os.path.splitext(os.path.basename(sample_file))[0]
            text_file = os.path.join(output_dir, f"{file_base}.txt")
            common.write_text(record_text, text_file)
             
            ann_file = os.path.join(output_dir, f"{file_base}.ann")
            common.write_text(self.READER.to_brat(), ann_file)
        
        if file_error_count:
            operations_logger.warning(f"Skipped outputs for {file_error_count} of {len(sample_files)} files with discrepant/missing annotations.")
        
        return file_error_count

    @staticmethod
    def __resolve_overlapping_annotations(orig_annotations: List[Annotation]) -> List[Annotation]:
        annot_by_aspect = defaultdict(list)
        for annotation in orig_annotations:
            annot_by_aspect[annotation.label].append(annotation)
        
        final_annotations = list()
        
        for annotations in annot_by_aspect.values():
            annotations = sorted(annotations, key=lambda a: a.spans[0])
            
            num_annotations = len(annotations)
            index = 0
            while index < num_annotations - 1:
                annot1 = annotations[index]
                annot2 = annotations[index + 1]
                
                range1 = annot1.spans[0]
                range2 = annot2.spans[0]
                if annot1.aspect == annot2.aspect:
                    if range1 == range2:    # remove if completely redundant
                        del annotations[index + 1]
                        num_annotations -= 1
                        continue
        
                    if range1[1] >= range2[0]:      # annotations are overlapping
                        if range1[1] >= range2[1]:  # first term full encapsulates second
                            del annotations[index + 1]
                            num_annotations -= 1
                            continue
                        
                        if range1[0] == range2[0] and range1[1] < range2[1]:    # second term full encapsulates first
                            del annotations[index]
                            num_annotations -= 1
                            continue
                
                index += 1
            
            final_annotations.extend(annotations)
        
        return sorted(final_annotations, key=lambda a: a.spans[0])


if __name__ == '__main__':
    unittest.main()
