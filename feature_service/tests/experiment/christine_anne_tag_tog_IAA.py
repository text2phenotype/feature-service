import os

from feature_service.active.annotator_disagreement import AnnotatorDisagreement
from feature_service.jobs.job_metadata import JobMetadata
from text2phenotype.common.data_source import DataSource

base_dir ='/Users/shannon.fee/Downloads/gold_tag_tog_extracted'
text_dir = 'tag_tog_text'
annotations_dir = 'tag_tog_annotations/IAA_christine_anne/2021-01-28'
christine_dir = 'cpersaud'

anne_dir = 'afrea'

args = {'annotator_disagreement':True, 'original_raw_text_dirs': ['mdl-phi-cyan-us-west-2'],
        'ann_dirs':[
            os.path.join(annotations_dir, anne_dir),
            os.path.join(annotations_dir, christine_dir)],
        'parent_dir': base_dir,
        'text_dir_prefix': text_dir


        }
data_source = DataSource(**args)
job_metadata = JobMetadata(**args)
ann_disagree = AnnotatorDisagreement(data_source=data_source, job_metadata=job_metadata)

ann_disagree.annotator_disagreement()