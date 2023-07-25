from typing import List

from feature_service.nlp import nlp_cache


def format_response(suggest=None, evidence=None):
    """
    :param suggest: auto-suggest an answer
    :param evidence: partial response from NLP auto-coder
    :return:
    """
    return {'suggest': suggest, 'evidence': evidence}


def complete_evidence(res, content='result') -> list:  # TODO: refactor : use HepcReader instead of manual JSON parsing
    """
    :param res: response from ctakes
    :param content: the field that contains the content of the response, e.g 'labValues' for hepc_lab_value
                'drugEntities' for
    :return: a list of evidence of that response
    """
    if len(res[content]) == 0:
        return None

    res_list = list()  # a list of dictionary that contains all the cuis in the response from one pipeline
    content_list = res[content]  # a list of dictionary as a value concept field in the response
    for i in range(len(content_list)):
        # for every concept hit in the content list
        concept = content_list[i]  # the ith concept of the content - a dictionary
        polarity = concept['attributes']['polarity']  # get the polarity of that concept
        for j in range(len(concept['umlsConcept'])):
            # for every umls hit of that concept
            umls_concept = concept['umlsConcept'][j]
            umls_concept['text'] = concept['text']
            umls_concept['polarity'] = polarity
            umls_concept['attributes'] = concept['attributes']
            del umls_concept['code']
            for clutter in ['polarity', 'generic', 'conditional', 'modality', 'uncertainty']:
                if clutter in umls_concept['attributes'].keys():
                    del umls_concept['attributes'][clutter]
            res_list.append(umls_concept)
    return res_list


def evidence_concept(text) -> List:
    """
    Return evidence of concepts matching text
    :param text: clinical text
    :return: evidence ( ctakes.hepc_clinical )
    """
    return complete_evidence(nlp_cache.hepc_clinical(text))


def evidence_lab_value(text) -> List:
    """
    Return evidence of HEPC LabValue matching text
    """
    return complete_evidence(nlp_cache.hepc_lab_value(text), 'labValues')


def evidence_drug_ner(text) -> List:
    """
    Return evidence of HEPC DrugNER matching text
    """
    return complete_evidence(nlp_cache.hepc_drug_ner(text), 'drugEntities')
