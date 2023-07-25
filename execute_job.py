import argparse
import ast
import json

from text2phenotype.constants.features import FeatureType

from feature_service.jobs.feature_service_job import FeatureServiceJob


def parse_arguments():
    """
    this parses the argument passed into the terminal
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-job_id', type=convert_string, help='identifier for job')
    parser.add_argument('-feature_set_annotate', type=convert_string, help='whether to label_annotations raw records')
    parser.add_argument('-label_annotations', type=convert_string, help='whether to label annotations')
    parser.add_argument('-update_annotation', type=convert_string, help='whether to update annotations')
    parser.add_argument('-feature_set_version', type=convert_string, help='Version for feature set annotation')
    parser.add_argument('-demographics_to_deid', type=convert_string, help='transform demographic jsons to deid jsons')
    parser.add_argument('-job_metadata', type=convert_string, help='metadata describing job')
    parser.add_argument('-model_label', type=convert_model_label, help='label indicating intended model usage')
    parser.add_argument('-add_annotation', type=convert_string, help='whether to add annotations')
    return parser.parse_args()


def convert_string(value: str):
    if value == 'None':
        value = None
    elif value in ['1', 'true', 'True', 'TRUE', 'yes', True]:
        value = True
    elif value in ['0', 'false', 'False', 'FALSE', 'no', None, False]:
        value = False
    elif value.startswith('[') and value.endswith(']'):
        value = ast.literal_eval(value)
    elif value.startswith('{') and value.endswith('}'):
        value = json.loads(value)
    return value


def convert_model_label(value: str):
    if value in {'None', None}:
        return None
    return FeatureType[value]


def prepare_metadata(args: dict):
    metadata = args.pop('job_metadata')
    for k, v in metadata.items():
        if k == 'model_label':
            v = convert_model_label(v)
        args[k] = v
    return args


if __name__ == '__main__':
    parsed_args = vars(parse_arguments())
    parsed_job_metadata = prepare_metadata(parsed_args)
    FeatureServiceJob(**parsed_job_metadata)
