from collections import defaultdict
from typing import (
    Dict,
    List,
)

from feature_service.feature_set.feature_cache import FeatureCache
from feature_service.features.feature import (
    Feature,
    FeatureConfigName,
)
from feature_service.hep_c import autofill
from feature_service.hep_c.form import (
    autofill_hepc_form,
    match_concepts,
)
from text2phenotype.common.log import operations_logger
from text2phenotype.constants.features import FeatureType


def get_question_key(section: str, question: str):
    return f'{section}//{question}'


def get_question_indices(grammar, target_sections):
    index = 1
    question_indices = dict()
    for section in target_sections:
        for question in sorted(grammar[section].keys()):
            question_indices[get_question_key(section, question)] = index
            index += 1
    return question_indices


class Form(Feature):
    feature_type = FeatureType.form
    target_sections = ['DEMOGRAPHICS', 'DIAGNOSIS_OTHER', 'LABORATORY_PANELS', 'LABORATORY_OTHER']
    grammar = Feature.Feature_Cache.hcv_grammar()
    question_indices = get_question_indices(grammar, target_sections)
    vector_length = len(question_indices) + 1
    config_name = FeatureConfigName.hepc

    def __init__(self):
        super().__init__()
        self.default_vector[0] = 1

    # @chunk_annotations()
    def annotate(self, text: str, fdl_data: dict = None, **kwargs):

        matches = defaultdict(list)

        if fdl_data:
            operations_logger.debug(f'Using FDL results for the '
                                    f'feature - {self.feature_type.value}, '
                                    f'config - {self.config_name.value}')
            data = self._update_data(fdl_data)
            res_list = []
            content_list = data['result']  # a list of dictionary as a value concept field in the response
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

            fill = defaultdict(list)
            feature_cache = FeatureCache()
            for section, questions in feature_cache.hcv_grammar().items():
                for question in questions:
                    for res in res_list:
                        cui_found = res.get('cui')

                        if match_concepts(question, cui_found):
                            auto_resp = autofill.format_response(question, res)
                            fill[section].append(auto_resp)
                            break
                    else:
                        fill[section].append(autofill.format_response(question, None))
        else:
            fill = autofill_hepc_form(text)

        for section in self.target_sections:
            self.__process_matches(fill[section], matches, section)
        return matches.items()

    def vectorize_token(self, token: dict, **kwargs):
        vector = self.zero_vector.copy()
        for match in token:
            vector[self.question_indices[match[FeatureType.form.name]]] = 1
        return vector

    @classmethod
    def __process_matches(cls, d_list: List[Dict], matches: Dict, section: str):
        for d in d_list:
            evidence = d.get('evidence')
            if not evidence:
                continue

            evidence = evidence.copy()
            matched_text = evidence['text']
            matches[(matched_text[1], matched_text[2])].append(
                {matched_text[0]: evidence, FeatureType.form.name: get_question_key(section, d['suggest'])})
            del evidence['text']
