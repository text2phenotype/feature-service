from typing import List

from text2phenotype.constants.features import FeatureType

from feature_service.constants import NPITypes
from feature_service.features.binary_feature import BinaryFeature
from feature_service.features.feature import Feature
from feature_service.nlp import nlp_cache

from text2phenotype.common.featureset_annotations import MachineAnnotation


MATCH_Addresses = ['mailingAddress', 'physicalAddress']
match_address_vals = ['street', 'city', 'state', 'zip']


class NPI(Feature):
    feature_type = FeatureType.npi
    vector_length = 10

    def annotate(self, text: str, **kwargs):
        """JIRA/BIOMED-270"""
        matches = dict()
        npi_sets = dict()
        response = nlp_cache.npi_recognition(text)

        # TODO: do we need to do nlp cache just as we did for clinical pipeline?
        for hit in response['providers']:
            _text = hit['text']
            _code = int(hit['code'])
            index = (_text[1], _text[2])
            _match_type = hit['match'].replace('address', '').replace('Mailing', '').replace(
                'Physical', '').replace('Name', '').strip()

            if not matches.get(index):
                matches[index] = {_match_type: {"count": 1, "codes": {_code}}}
            elif _match_type in matches[index]:
                matches[index][_match_type]['count'] += 1
                matches[index][_match_type]["codes"].add(_code)
            else:
                matches[index][_match_type] = {"count": 1, "codes": {_code}}

            if _match_type in npi_sets:
                npi_sets[_match_type].add(_code)
            else:
                npi_sets[_match_type] = {_code}

        for index, annotated_npi in matches.items():

            for match_type, code_count in annotated_npi.items():
                matches[index][match_type]['codes'] = list(code_count['codes'])

                for npi_k, npi_v in npi_sets.items():
                    if match_type != npi_k:
                        _intersection = npi_v.intersection(code_count['codes'])
                        if _intersection:
                            matches[index][match_type][npi_k] = list(_intersection)

        return matches.items()

    def vectorize_token(self, token, **kwargs) -> List[int]:
        """
        ALL BINARY
        * provider name direct match
        * facility name direct match
        * street direct match
        * phone direct match
        * fax direct match
        * npi matches a provider name somewhere else in document
        * npi matches a facility name somewhere else in document
        * npi matches a phone somewhere else in document
        * npi matches a fax somewhere else in document
        * npi matches a street name somewhere else in document
        :param **kwargs:
        """

        vector = self.default_vector.copy()

        for npi_label in NPITypes:
            if npi_label.name in token[0]:
                vector[npi_label.value] = 1
                for k in token[0][npi_label.name].keys():
                    if k in NPITypes.__members__:
                        vector[len(NPITypes.__members__) + NPITypes[k].value] = 1

        return vector


class NPIBinary(BinaryFeature, NPI):
    feature_type = FeatureType.npi_binary
    annotated_feature = FeatureType.npi

    def vectorize_token(self, token, **kwargs) -> List[int]:
        if token:
            vector = self.default_vector.copy()

            for npi_label in NPITypes:
                if npi_label.name in token[0]:
                    vector[0] = 1

                    break

            return vector
