from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict

from feature_service.feature_set.feature_cache import FeatureCache
from feature_service.features.feature import FeatureConfigName
from feature_service.features.feature import Feature
from feature_service.nlp import nlp_cache
from text2phenotype.common.log import operations_logger
from text2phenotype.constants.features import (
    DocumentTypeLabel,
    FeatureType,
)


class _Attributes:
    __attr_list = [
        ('match', {'strict': 0, 'abbr': 1, 'pref': 2, 'relax': 3}),
        ('impress', {'interpret': 0, 'first': 1, 'conclude': 2, 'notable': 3, 'ignore': 4, 'second': 5}),
        ('when', {'admit': 0, 'history': 1, 'present': 2, 'plan': 3, 'discharge': 4, 'transfer': 5}),
        ('who', {'patient': 0, 'family': 1, 'provider': 2, 'insurance': 3}),
        ('rank', {'high': 0, 'ignore': 1, 'first': 2, 'second': 3, 'low': 4}),
        ('style', {'narrative': 0, 'subhead': 1, 'lists': 2, 'printer': 3, 'choice': 4, 'legal': 5, 'calendar': 6, 'unique': 7}),
        ('visit', {'encounter': 0, 'social': 1, 'demographics': 2}),
        ('where', {'hosp': 0, 'home': 1, 'outpatient': 2, 'surgery': 3, 'consult': 4, 'department': 5, 'radiology': 6, 'pathology': 7, 'emergency': 8, 'clinic': 9}),
        ('instruct', {'care': 0, 'cover': 1}),
        ('drug', {'med': 0, 'immunization': 1, 'allergy': 2}),
        ('measure', {'finding': 0, 'lab': 1, 'imaging': 2, 'objective': 3, 'vital': 4}),
        ('why', {'complaint': 0, 'indication': 1, 'reason': 2}),
        ('exam', {'physical': 0, 'ros': 1}),
        ('problem', {'symptom': 0, 'problem': 1, 'diagnosis': 2}),
        ('procedure', {'operate': 0, 'procedure': 1, 'device': 2})
    ]
    __bin_attrs = {'multi', 'common'}
    length = sum(len(a[1]) for a in __attr_list) + len(__bin_attrs)

    def __init__(self, code, term, attr):
        self.code = code
        self.term = term
        self.__attr = attr

    def vectorize(self):
        vector = [0] * self.length

        offset = 0
        for a in self.__bin_attrs:
            if a in self.__attr:
                vector[offset] = 1

            offset += 1

        for key, values in self.__attr_list:
            if key in self.__attr:
                vector[offset + values[self.__attr[key]]] = 1

            offset += len(values)

        return vector


class _Sections:
    def __init__(self):
        self.__sections = self.__init_sections()

    def __len__(self):
        return len(self.__sections)

    def __iter__(self):
        for code, concepts in sorted(self.__sections.items()):
            yield code, concepts

    def __getitem__(self, item):
        return self.__sections[item]

    def __contains__(self, item):
        return item in self.__sections

    def __init_sections(self):
        sections = defaultdict(dict)

        # code -> phrase -> attributes
        for code, phrases in FeatureCache().loinc_sections().items():
            for phrase, attributes in phrases.items():
                sections[code][phrase.upper()] = _Attributes(code, phrase, attributes)

        return sections


sections = _Sections()


class _LoincFeature(Feature, ABC):
    attributes = 'attributes'
    umlsConcept = 'umlsConcept'
    polarity = 'polarity'
    vector_length = 1

    def annotate(self, text: str, fdl_data: dict = None, **kwargs):
        if fdl_data:
            data = fdl_data
            operations_logger.debug(f'Using FDL results for the '
                                    f'feature - {self.feature_type.value}, '
                                    f'config - {self.config_name.value}')
        else:
            data = self._annotate(text)

        matches = defaultdict(list)
        for hit in data['result']:
            _text = hit['text']
            index = (_text[1], _text[2])

            if text[_text[1]: _text[2]].lower() != _text[0].lower():
                operations_logger.debug("wrong range for the hit")
                continue

            matches[index].append({
                'text': _text,
                self.attributes: hit[self.attributes],
                self.umlsConcept: hit[self.umlsConcept]
            })

        return matches.items()

    @abstractmethod
    def _annotate(self, text: str):
        pass

    def vectorize_token(self, token, **kwargs):
        vector = self.default_vector.copy()

        if token[0].get(self.attributes, {}).get(self.polarity, {}) == 'positive':
            vector[0] = 1

        return vector


class LoincSection(_LoincFeature):
    feature_type = FeatureType.loinc_section
    vector_length = 1 + len(sections)
    loinc_code_map = {code: i for i, (code, _) in enumerate(sections)}
    config_name = FeatureConfigName.loinc_section

    def _annotate(self, text: str):
        return nlp_cache.loinc_section(text)

    def vectorize_token(self, token, **kwargs):
        vector = super().vectorize_token(token, **kwargs)

        code = self.get_loinc_code(token)
        if code in self.loinc_code_map:
            vector[1 + self.loinc_code_map[code]] = 1

        return vector

    @classmethod
    def get_loinc_code(cls, annotation):
        return annotation[0][cls.umlsConcept][0]['cui']


class LoincTitle(_LoincFeature):
    feature_type = FeatureType.loinc_title
    config_name = FeatureConfigName.loinc_title

    def vectorize_token(self, token, **kwargs):
        vector = super().vectorize_token(token, **kwargs)

        # TODO: need to figure out
        return vector

    def _annotate(self, text: str):
        return nlp_cache.loinc_title(text)


class LoincSectionAttributes(Feature):
    annotated_feature = FeatureType.loinc_section
    feature_type = FeatureType.loinc_section_attributes
    vector_length: int = _Attributes.length
    requires_annotation = False

    def vectorize_token(self, token, **kwargs):
        code = LoincSection.get_loinc_code(token)
        if code in sections:
            term = token[0]['text'][0].upper()
            section = sections[code]

            if term in section:
                return section[term].vectorize()


class LoincSectionDocTypes(Feature):
    annotated_feature = FeatureType.loinc_section
    feature_type = FeatureType.loinc_section_doc_types
    vector_length: int = len(DocumentTypeLabel) - 1
    requires_annotation = False

    def __init__(self):
        super().__init__()
        self.__sections = self.__load_doc_section_map()

    def vectorize_token(self, token, **kwargs):
        code = LoincSection.get_loinc_code(token)
        vector = self.default_vector.copy()

        for doc_type in self.__sections[code]:
            vector[doc_type.value.column_index - 1] = 1

        return vector

    @staticmethod
    def __load_doc_section_map():
        doc_map = {'progress_note': DocumentTypeLabel.progress_notes,
                   'history_and_physical_note': DocumentTypeLabel.history_and_physical,
                   'diagnostic_imaging_study': DocumentTypeLabel.diagnostic_imaging_study,
                   'procedure_note': DocumentTypeLabel.procedure_note,
                   'surgical_operation_note': DocumentTypeLabel.surgical_operation_note,
                   'consult_note': DocumentTypeLabel.consult_note,
                   'discharge_summary': DocumentTypeLabel.discharge_summary,
                   'pathology_report': DocumentTypeLabel.pathology,
                   'coversheet': DocumentTypeLabel.non_clinical}

        section_map = defaultdict(set)

        for doc_type, doc_info in FeatureCache().loinc_doc_sections().items():
            if doc_type not in doc_map:
                continue

            doc_type = doc_map[doc_type]

            for code in doc_info['sections'].keys():
                section_map[code].add(doc_type)

        return section_map
