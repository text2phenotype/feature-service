from collections import defaultdict
from typing import List

from text2phenotype.tagtog.tag_tog_annotation import TagTogEntity, TagTogAnnotationSet

from feature_service.active.annotator_disagreement import AnnotatorDisagreement
from text2phenotype.tagtog.tag_tog_client import TagTogClient
from text2phenotype.tagtog.helper_functions import add_tag_tog_annotation_to_doc_id

DISAGREE_FIELD_NAME = 'disagree' # must exactly match a boolean entity label in the tag tog project,
# if provided will label all disagreed upon labels as "disagree" otherwise will simply merge the union of all annotations
MEMBERS_ANNCOMPLETE = 'members_anncomplete'


def merge_tag_tog_annotations(annotation_list: List[TagTogAnnotationSet], disagree_field_id: str = None):
    positions = list()
    annotators = list(range(len(annotation_list)))
    pointers = [0] * len(annotation_list)
    # get list of all parts used for annotations
    all_parts = set()
    for annotation in annotation_list:
        all_parts.update({entry.part for entry in annotation.entities})
    for part in all_parts:
        full_entity_list = []

        for ann_set in annotation_list:
            positions.append(ann_set.to_positions_for_disagree(part=part))

        overlap_pos = AnnotatorDisagreement.get_overlap_doc(
            positions,
            pointers=pointers,
            ann_fps=annotators)

        full_entity_list.extend(
            create_tag_tog_annot_from_overlap_pos(
                overlap_pos,
                annotators=annotators,
                part=part,
                disagree_field_name=disagree_field_id))

        tag_tog_annotation_set = TagTogAnnotationSet(entities=full_entity_list)

    return tag_tog_annotation_set


def create_tag_tog_annot_from_overlap_pos(
        overlap_pos: List[dict],
        annotators: list,
        disagree_field_name: str = None,
        part: str = 's1v1'
):
    output = list()
    for entry in overlap_pos:
        votes = defaultdict(list)
        for member_id in annotators:
            if member_id in entry:
                votes[entry[member_id]].append(member_id)

        # choose most popular non na label
        label = sorted(
            {k: v for k, v in votes.items() if k != 'na'},
            key=lambda x: len(votes[x])
        )[-1]

        # if there is disagreement and a disagree field name, add info
        fields = {}
        if len(votes) > 1:
            if disagree_field_name:
                fields = {
                    disagree_field_name: {
                        "value": True,
                        "confidence": {
                            "state": "pre-added",
                            "who": ["user:tagtogadmin"],
                            "prob": 1
                        }
                    }
                }
        tt_ent = TagTogEntity(
            text_range=entry['range'],
            text=entry['text'],
            classId=label,
            part=part,
            fields=fields)
        output.append(tt_ent)

    return output


# run_merge_tag_tog_annots(require_complete=False,  folder_name='us-west-2')

def merge_push_tag_tog_annots_client(tc_client: TagTogClient, subfolder: str):
    files = tc_client.search(f'folder:{subfolder}')
    for file in files:
        # only merge annotations where multiple users have marked a file as complete
        if len(file.get(MEMBERS_ANNCOMPLETE)) > 1:
            member_ids = file.get(MEMBERS_ANNCOMPLETE)
            if len(member_ids) > 2:
                member_ids = [member for member in member_ids if member != 'CEPuser']
            file_id = file.get('id')
            ann_json_raw = [
                tc_client.get_member_annjson(member=member, doc_id=file_id)for member in member_ids]
            ann_jsons = [
                TagTogAnnotationSet(raw_json.json()) for raw_json in ann_json_raw if raw_json.ok]

            if len(ann_jsons) > 1:
                disagree_field_label = tc_client.inverse_annotation_legend.get(DISAGREE_FIELD_NAME)

                merged_ann_json = merge_tag_tog_annotations(ann_jsons, disagree_field_id=disagree_field_label)

                # push back up to tag tog
                add_tag_tog_annotation_to_doc_id(ann_json=merged_ann_json, doc_id=file_id, tag_tog_client=tc_client)


# TO RUN MERGE TAG TOG ANNOTATIONS FROM TAG TOG,
# PUSHES ALL MERGED FILES THAT HAVE MULTIPLE LABELS CONFIRMEDTO THE MASTER COPY WITH A LBEL OF DISAGREE IF ONE EXISTS FOR THE PREOJECT
# tc_client = TagTogClient(project='diagnosis_signsymptom_validation', proj_owner='tagtogadmin')
# merge_push_tag_tog_annots_client(tc_client=tc_client, subfolder='mdl-phi-cyan-us-west-2')

