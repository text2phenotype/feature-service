import os

from text2phenotype.common import common
from text2phenotype.annotations.file_helpers import Annotation, AnnotationSet

OUTBOX_PATH = "/opt/S3/us-west-2/outbox/mimic/processed/documents"

MIMIC_BASE_PATH = (
    "mimic/"
    "shareclef-ehealth-evaluation-lab-2014-task-2-disorder-attributes-in-clinical-reports-1.0/20200306"
)

MIMIC_FULL_TEXT_PATH = os.path.join(
    "/opt/S3/biomed-data/",
    MIMIC_BASE_PATH
)

MIMIC_ANNOTATIONS_PATH = os.path.join(
    "/opt/S3/biomed-data/annotations/",
    MIMIC_BASE_PATH
)

OUTPUT_ANNOTATION_ROOT = "/opt/S3/annotations/"


def check_range_overlap(rng1, rng2):
    # boolean to check if two ranges overlap
    return rng1[0] <= rng2[1] and rng2[0] <= rng1[1]


def main():
    doc_uuids = os.listdir(OUTBOX_PATH)

    for doc_id in doc_uuids:
        doc_path = os.path.join(OUTBOX_PATH, doc_id)

        # extract the original filename from the metadata to match to the original annotation
        metadata_filename = f"{doc_id}.metadata.json"
        metadata_dict = common.read_json(os.path.join(doc_path, metadata_filename))
        mimic_file_path_no_ext = metadata_dict['document_info']['source'][len("inbox/"):]
        mimic_file_path_no_ext, _ = os.path.splitext(mimic_file_path_no_ext)
        mimic_path, mimic_filename_no_ext = os.path.split(mimic_file_path_no_ext)
        _, mimic_subtask_path = os.path.split(mimic_path)

        ann_filename = mimic_filename_no_ext + ".ann"

        # load the original annotation for this file
        ann_content = common.read_text(os.path.join(
            MIMIC_ANNOTATIONS_PATH,
            mimic_subtask_path,
            ann_filename
        ))
        # should confirm that annotations are sorted!
        ann_set_orig = AnnotationSet.from_file_content(ann_content)
        ann_set_orig_list = sorted(ann_set_orig.entries, key=lambda x: x.text_range)

        # load the machine annotation json
        summary_filename = f"{doc_id}.clinical_summary.json"
        clinical_summary = common.read_json(os.path.join(doc_path, summary_filename))

        diagnosis_clinical_summary = clinical_summary['DiseaseDisorder']
        signsymptom_clinical_summary = clinical_summary['SignSymptom']

        diagnosis_machine_ann_list = [
            Annotation(
                label=ann_dict["label"],
                text=ann_dict["text"],
                text_range=ann_dict["range"],
                coord_uuids=None,
                line_start=None,
                line_stop=None,
                category_label=None
            )
            for ann_dict in diagnosis_clinical_summary
        ]
        # make sure annotations are sorted by range
        diagnosis_machine_ann_list = sorted(diagnosis_machine_ann_list, key=lambda x: x.text_range)

        signsymptom_machine_ann_list = [
            Annotation(
                label=ann_dict["label"],
                text=ann_dict["text"],
                text_range=ann_dict["range"],
                coord_uuids=None,
                line_start=None,
                line_stop=None,
                category_label=None
            )
            for ann_dict in signsymptom_clinical_summary
        ]
        # make sure annotations are sorted by range
        signsymptom_machine_ann_list = sorted(signsymptom_machine_ann_list, key=lambda x: x.text_range)

        # look for overlap on joined labels
        # doing this in O(n^2), smarter would be keeping a pointer on sorted lists
        matched_anns = []
        for old_ann in ann_set_orig_list:
            for machine_ann in diagnosis_machine_ann_list:
                if check_range_overlap(machine_ann.text_range, old_ann.text_range):
                    matched_anns.append((old_ann, machine_ann))

        # keep the machine annotation matches for now, even though they may have more tokens in a label
        machine_ann_diagnosis = [machine_ann for old_ann, machine_ann in matched_anns]
        # add the sign_symptom machine annotations
        machine_human_annotations = sorted(
            signsymptom_machine_ann_list + machine_ann_diagnosis, key=lambda x: x.text_range)
        machine_human_ann_set = AnnotationSet.from_list(machine_human_annotations)
        machine_ann_set = AnnotationSet.from_list(
            sorted(diagnosis_machine_ann_list + signsymptom_machine_ann_list, key=lambda x: x.text_range)
        )

        # create file for just the machine labels
        machine_only_path = os.path.join(
            OUTPUT_ANNOTATION_ROOT,
            "diagnosis_symptom_machine",
            MIMIC_BASE_PATH,
            mimic_subtask_path,
        )
        os.makedirs(machine_only_path, exist_ok=True)
        ann_file_out_path = os.path.join(machine_only_path, ann_filename)
        content = machine_ann_set.to_file_content()
        common.write_text(content, ann_file_out_path)
        print(f"Wrote {len(machine_ann_set)} labels to output file: {ann_file_out_path}")

        # create file with the subset of human-confirmed diagnosis labels + signsymptom machine labels
        human_machine_path = os.path.join(
            OUTPUT_ANNOTATION_ROOT,
            "diagnosis_symptom_human_machine",
            MIMIC_BASE_PATH,
            mimic_subtask_path,
        )
        os.makedirs(human_machine_path, exist_ok=True)
        ann_file_out_path = os.path.join(human_machine_path, ann_filename)
        content = machine_human_ann_set.to_file_content()
        common.write_text(content, ann_file_out_path)
        print(f"Wrote {len(machine_human_ann_set)} labels to output file: {ann_file_out_path}")

    print(f"Finished writing {len(doc_uuids)} files to : {OUTPUT_ANNOTATION_ROOT}")


if __name__ == "__main__":
    main()
