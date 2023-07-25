import unittest

import pandas as pd

from feature_service.active.annotator_disagreement import AnnotatorDisagreement


class TestAnnotatorDisagreement(unittest.TestCase):
    ann_dirs = [
        "annotations/anne.frea",
        "annotations/satjiv.kohli",
        "annotations/despina.siolas"
    ]
    counts = [8204, 2365, 6679]
    annotator_total_token_counts = pd.Series({k: v for k,v in zip(ann_dirs, counts)})
    labels_no_na = ["diagnosis", "signsymptom"]

    def test_vote_agree(self):
        target_label = "diagnosis"
        ann_dict = {k: target_label for k in self.ann_dirs}
        ann_dict[self.ann_dirs[0]] = AnnotatorDisagreement.NA_LABEL
        ann_dict.update({
            "is_diagnosis": True,
            "is_signsymptom": False,
            "pos_disagree": False
        })
        annotation_row = pd.Series(ann_dict)
        label_out = AnnotatorDisagreement.vote(
            annotation_row, self.ann_dirs, self.annotator_total_token_counts, self.labels_no_na)
        self.assertEqual(target_label, label_out)

    def test_vote_disagree_no_join(self):
        target_label = "diagnosis"

        # highest ranked voter wins equal vote
        found_labels = ["diagnosis", "na", "signsymptom"]
        ann_dict = {k: v for k, v in zip(self.ann_dirs, found_labels)}
        ann_dict.update({
            "is_diagnosis": False,
            "is_signsymptom": False,
            "pos_disagree": True
        })
        annotation_row = pd.Series(ann_dict)
        label_out = AnnotatorDisagreement.vote(
            annotation_row, self.ann_dirs, self.annotator_total_token_counts, self.labels_no_na)
        self.assertEqual(target_label, label_out)

        # highest ranked voter disagrees with majority
        found_labels = ["signsymptom", "diagnosis", "diagnosis"]
        ann_dict = {k: v for k, v in zip(self.ann_dirs, found_labels)}
        ann_dict.update({
            "is_diagnosis": False,
            "is_signsymptom": False,
            "pos_disagree": True
        })
        annotation_row = pd.Series(ann_dict)
        label_out = AnnotatorDisagreement.vote(
            annotation_row, self.ann_dirs, self.annotator_total_token_counts, self.labels_no_na)
        self.assertEqual(target_label, label_out)

        # highest ranked voter didnt label, next highest gets it right
        found_labels = ["na", "signsymptom", "diagnosis"]
        ann_dict = {k: v for k, v in zip(self.ann_dirs, found_labels)}
        ann_dict.update({
            "is_diagnosis": False,
            "is_signsymptom": False,
            "pos_disagree": True
        })
        annotation_row = pd.Series(ann_dict)
        label_out = AnnotatorDisagreement.vote(
            annotation_row, self.ann_dirs, self.annotator_total_token_counts, self.labels_no_na)
        self.assertEqual(target_label, label_out)

    def test_vote_disagree_join(self):
        target_label = "signsymptom"
        found_labels = [
            "signsymptom,na,signsymptom,na,na",
            "diagnosis,diagnosis,diagnosis,diagnosis,diagnosis",
            "signsymptom,signsymptom,signsymptom,na,na"
        ]
        ann_dict = {k: v for k, v in zip(self.ann_dirs, found_labels)}
        ann_dict.update({
            "is_diagnosis": False,
            "is_signsymptom": False,
            "pos_disagree": True
        })
        annotation_row = pd.Series(ann_dict)
        label_out = AnnotatorDisagreement.vote(
            annotation_row, self.ann_dirs, self.annotator_total_token_counts, self.labels_no_na)
        self.assertEqual(target_label, label_out)

        # highest ranked voter didnt vote
        target_label = "signsymptom"
        found_labels = [
            "na,na,na,na,na",
            "diagnosis,diagnosis,diagnosis,diagnosis,diagnosis",
            "signsymptom,signsymptom,signsymptom,na,na"
        ]
        ann_dict = {k: v for k, v in zip(self.ann_dirs, found_labels)}
        ann_dict.update({
            "is_diagnosis": False,
            "is_signsymptom": False,
            "pos_disagree": True
        })
        annotation_row = pd.Series(ann_dict)
        label_out = AnnotatorDisagreement.vote(
            annotation_row, self.ann_dirs, self.annotator_total_token_counts, self.labels_no_na)
        self.assertEqual(target_label, label_out)

        # highest ranked voter didnt vote, winner has more na than label
        target_label = "signsymptom"
        found_labels = [
            "na,na,na,na,na",
            "diagnosis,diagnosis,diagnosis,diagnosis,diagnosis",
            "signsymptom,signsymptom,na,na,na"
        ]
        ann_dict = {k: v for k, v in zip(self.ann_dirs, found_labels)}
        ann_dict.update({
            "is_diagnosis": False,
            "is_signsymptom": False,
            "pos_disagree": True
        })
        annotation_row = pd.Series(ann_dict)
        label_out = AnnotatorDisagreement.vote(
            annotation_row, self.ann_dirs, self.annotator_total_token_counts, self.labels_no_na)
        self.assertEqual(target_label, label_out)

    def test_vote_join_degenerate(self):
        # degenerative case, shouldn't get this but need to handle it
        target_label = "signsymptom"
        found_labels = [
            "signsymptom,na,signsymptom,na,na",
            "diagnosis,diagnosis,diagnosis,diagnosis,diagnosis",
            "signsymptom,signsymptom,na,diagnosis,diagnosis"
        ]
        ann_dict = {k: v for k, v in zip(self.ann_dirs, found_labels)}
        ann_dict.update({
            "is_diagnosis": False,
            "is_signsymptom": False,
            "pos_disagree": True
        })
        annotation_row = pd.Series(ann_dict)
        label_out = AnnotatorDisagreement.vote(
            annotation_row, self.ann_dirs, self.annotator_total_token_counts, self.labels_no_na)
        self.assertEqual(target_label, label_out)

        # degenerative case, shouldn't get this but need to handle it
        target_label = "diagnosis"
        found_labels = [
            "na,na,na,na,na",
            "diagnosis,diagnosis,diagnosis,diagnosis,diagnosis",
            "signsymptom,signsymptom,signsymptom,diagnosis,diagnosis"
        ]
        ann_dict = {k: v for k, v in zip(self.ann_dirs, found_labels)}
        ann_dict.update({
            "is_diagnosis": False,
            "is_signsymptom": False,
            "pos_disagree": True
        })
        annotation_row = pd.Series(ann_dict)
        label_out = AnnotatorDisagreement.vote(
            annotation_row, self.ann_dirs, self.annotator_total_token_counts, self.labels_no_na)
        self.assertEqual(target_label, label_out)

    def test_vote_degenerate(self):
        target_label = AnnotatorDisagreement.NA_LABEL
        found_labels = ["na", "na", "na"]
        ann_dict = {k: v for k, v in zip(self.ann_dirs, found_labels)}
        # should not get a case where all three are False, but here we are
        ann_dict.update({
            "is_diagnosis": False,
            "is_signsymptom": False,
            "pos_disagree": False
        })
        annotation_row = pd.Series(ann_dict)
        label_out = AnnotatorDisagreement.vote(
            annotation_row, self.ann_dirs, self.annotator_total_token_counts, self.labels_no_na)
        self.assertEqual(target_label, label_out)


if __name__ == '__main__':
    unittest.main()
