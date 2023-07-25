from collections import defaultdict
from typing import Dict, List

from feature_service.hep_c import autofill
from feature_service.feature_set.feature_cache import FeatureCache


def autofill_hepc_form(text) -> Dict:
    """
    this function takes in clinical text
    :param text: clinical text
    :return: HepC Json format with suggested answer and evidence for each question
    """
    form = defaultdict(list)
    results = get_evidence(text)
    feature_cache = FeatureCache()

    for section, questions in feature_cache.hcv_grammar().items():
        for question in questions:
            for res in results:
                cui_found = res.get('cui')

                if match_concepts(question, cui_found):
                    auto_resp = autofill.format_response(question, res)
                    form[section].append(auto_resp)
                    break
            else:
                form[section].append(autofill.format_response(question, None))

    return form


def get_evidence(text) -> List:
    """
    :param text: clinical text
    :return: a list of all umls evidence of the this clinical text
    """
    res = list()

    check_box = autofill.evidence_concept(text)
    drug_ner = autofill.evidence_drug_ner(text)
    lab_value = autofill.evidence_lab_value(text)

    if lab_value:
        res.extend(lab_value)

    if drug_ner:
        res.extend(drug_ner)

    if check_box:
        res.extend(check_box)

    return res


def match_concepts(question, cui) -> bool:
    """
    To see if there are any cuis that falls into the question's cui list
    :param question: a question in the hepc form
    :param cui: a list of cuis that is returned
    :return: True, False or not found for this question
    """
    feature_cache = FeatureCache()
    cui_allowed = feature_cache.hep_c_answers().concepts(question)
    if cui_allowed and cui in cui_allowed:
        return True

    return False
