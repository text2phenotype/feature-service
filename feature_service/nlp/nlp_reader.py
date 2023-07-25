from typing import Dict, List, Set, Tuple

from text2phenotype.entity.attributes import Serializable, DocumentAttributes, TextSpan
from text2phenotype.entity.entity import LabEntity
from text2phenotype.entity.results import ResultList, Result, ResultType
from text2phenotype.entity.concept import Concept
from text2phenotype.common.errors import Text2phenotypeError

from feature_service.nlp import nlp_cache, autocode

###############################################################################
#
# default_clinical
#
###############################################################################


class ClinicalReader(Serializable):

    def __init__(self, source=None, autocoder=nlp_cache.clinical, result_type=ResultType.clinical):
        self.meta = None
        self.results = None
        self.result_type = result_type
        self.__autocoder = autocoder

        self.autocode(source)

    def __iter__(self):
        return iter(self.results)

    @staticmethod
    def init(source, pipeline=autocode.clinical):
        """
        :param source: text or Dict/JSON
        :param pipeline: pipeline to run if source is text
        :return: source (initialized)
        """
        if source is None:
            return None

        if isinstance(source, str):  # source= 'Myocardial Infarction'
            return pipeline(source)

        if isinstance(source, dict):  # source= nlp.autocoder.result
            return source

        if isinstance(source, list):  # source= TextMatch,[text,start,stop]
            return source

        raise Text2phenotypeError(f"source {source} was unexpected type {type(source)}")

    def autocode(self, source: str):
        if source:
            source = self.init(source, self.__autocoder)
            self.from_json(source)

    def to_table(self, tab='\t'):
        out = [""]
        if self.results:
            for r in self.results:
                out.append('')
                out.append(f'{self.result_type}')
                for child in r.to_table(tab):
                    out.append(child)
        return out

    def from_json(self, source: Dict):
        self.meta = DocumentAttributes(source)
        self.results = ResultList(source, self.result_type)

    def to_json(self) -> Dict:
        out = self.meta.to_json()
        out[self.result_type] = self.results.to_json()
        return out

    # LIST Result
    def list_results(self) -> List[Result]:
        return self.results.items

    def list_result_text(self) -> List[str]:
        return [r.match.text for r in self.list_results()]

    def longest(self) -> str:
        """
        :return: string of longest match
        """
        longest = ''
        for text in self.list_result_text():
            if not longest:
                longest = text
            if len(text) == len(longest):
                if text < longest: #UPPERCASE ordering
                    longest = text
            if len(text) > len(longest):
                longest = text
        return longest.strip()

    # LIST Clinical
    def list_concepts(self) -> List[Concept]:
        out = list()
        for r in self.list_results():
            for c in r.concepts:
                out.append(c)
        return out

    def list_concept_cuis(self) -> List[str]:
        """
        :return: list of concept unique identifiers
        """
        return [c.cui for c in self.list_concepts()]

    def list_concept_tuis(self) -> List[str]:
        """
        :return: list of concept semantic type identifiers
        """
        tuis = []
        for c in self.list_concepts():
            tuis.extend(c.tui)
        return tuis

    def list_concept_text(self) -> List[str]:
        """
        :return: list of concept preferredText
        """
        return [c.preferredText for c in self.list_concepts()]

    def list_concept_vocab(self) -> List[str]:
        """
        :return: list of concept vocabulary (codingScheme)
        """
        return [c.codingScheme for c in self.list_concepts()]

    def list_concepts_json(self):
        """
        :return: list of concepts as json
        """
        return [c.to_json() for c in self.list_concepts()]

    # UNIQ
    def uniq_result_text(self) -> Set[str]:
        """
        :return: set, see list_result_text
        """
        return set(self.list_result_text())

    def uniq_concept_cuis(self) -> Set[str]:
        """
        :return: set, see list_concept_cuis
        """
        return set(self.list_concept_cuis())

    def uniq_concept_text(self) -> Set[str]:
        """
        :return: set, list_concept_text
        """
        return set(self.list_concept_text())

    def uniq_concept_vocab(self) -> Set[str]:
        """
        :return: set, list_concept_vocab
        """
        return set(self.list_concept_vocab())

    # COUNT
    def count_results(self) -> int:
        return len(self.list_results())

    def count_concepts(self) -> int:
        return len(self.list_concepts())

    # MATCH
    def match_result(self, text) -> List[Result]:
        return [r for r in self.list_results() if text == r.match]

    def match_concept(self, preferred: TextSpan) -> List[Concept]:
        """
        :param preferred: matches PreferredText
        :return: concepts with this
        """
        return [c for c in self.list_concepts() if preferred == c.preferredText]

    def match_concept_cui(self, cui):
        return [c for c in self.list_concepts() if c.cui == cui]

    def match_text(self, text):
        return text in self.uniq_result_text()


###############################################################################
#
# drug_ner
#
###############################################################################
class DrugReader(ClinicalReader):
    def __init__(self, source=None, autocoder=nlp_cache.drug_ner):
        super().__init__(source, autocoder, ResultType.drug_ner)


###############################################################################
#
# lab_value
#
###############################################################################
class LabReader(ClinicalReader):
    """
    BIOMED-1402 Production default labels for lab values are used by summary:

    biomed.summary.pref_terms.summary_lab_value(
    FeatureType.lab_hepc.name

    Therefore the default autocoder is hepc_lab_value.

    See also FEATURES_FOR_REPRESENTATION = {
        FeatureType.lab_hepc,
        FeatureType.drug_rxnorm,
        FeatureType.clinical }

    see also: autocode.py
    see also: nlp_cache.py
    see also: LabReader(ClinicalReader)
    see also: HepcLabReader
    """
    def __init__(self, source=None, autocoder=nlp_cache.hepc_lab_value):
        super().__init__(source, autocoder, ResultType.lab_value)

    def list_labs(self) -> List[LabEntity]:
        if not self.results or len(self.results.items) == 0:
            return list()

        out = list()
        for res in self.results.items:
            out.append(
                LabEntity(text=res.match.text,
                          value=res.attributes.labValue.text,
                          units=res.attributes.labValueUnit.text,
                          polarity=res.attributes.polarity))
        return out

    # LIST Lab
    def list_lab_text(self) -> List:
        return [v.text for v in self.list_labs()]

    def list_lab_values(self) -> List:
        return [v.value for v in self.list_labs()]

    def list_lab_units(self) -> List:
        return [v.units for v in self.list_labs()]

    def list_lab_ranges(self) -> List:
        for _ in self.list_labs():
            pass
        return None

    # UNIQ Lab
    def uniq_lab_text(self) -> Set:
        return set(self.list_lab_text())

    def uniq_lab_values(self) -> Set:
        return set(self.list_lab_values())

    def uniq_lab_units(self) -> Set:
        return set(self.list_lab_units())

    # COUNT
    def count_labs(self) -> int:
        return len(self.list_labs())

    def first_lab(self) -> LabEntity:
        return self.list_labs()[0]


###############################################################################
#
# HEPC
#
###############################################################################
class HepcReader(ClinicalReader):
    def __init__(self, source=None, autocoder=nlp_cache.hepc_clinical):
        super().__init__(source, autocoder)


class HepcLabReader(LabReader):
    """
    BIOMED-1402: default lab reader is now HepcLabReader
    """
    def __init__(self, source=None, autocoder=nlp_cache.hepc_lab_value):
        super().__init__(source, autocoder)


class HepcDrugReader(DrugReader):
    def __init__(self, source=None, autocoder=nlp_cache.hepc_drug_ner):
        super().__init__(source, autocoder)


###############################################################################
#
# GUARD
#
###############################################################################
def guard_tuple(obj) -> Tuple:
    if isinstance(obj, tuple):
        return obj

    if isinstance(obj, list):
        if len(obj) != 2:
            raise IndexError(f"list could not be cast as Tuple, invalid len {len(obj)}")
        return obj[0], obj[1]

    raise TypeError(f'wrong type, expected Tuple, was {type(obj)}')


def guard_tuple_span(obj) -> Tuple:
    obj = guard_tuple(obj)

    int(obj[0])
    int(obj[1])

    return obj


###############################################################################
#
# Match Reader
#
###############################################################################

class MatchReader(Serializable):

    def __init__(self, source=None):
        self.spans = list()
        self.results = list()

        if source:
            self.from_json(source)

    def from_json(self, source):

        for found in source:
            span, match = found
            self.spans.append(span)
            self.results.append(match)

    def list_spans(self) -> List[Tuple]:
        """
        positions
        :return: List(Tuple(start,stop))
        """
        return self.spans

    def list_results(self) -> List[List]:
        return self.results

    def list_result_keys(self) -> List:
        """
        Example match_regex()
        :return: [$PATIENT_NAME, $DATE2, ....]
        """
        keys = list()
        for r in self.results:
            for hit in r:
                for k, v in hit.items():
                    keys.append(k)
        return keys

    def list_result_values(self):
        """
        Example match_regex()
        :return [01/02/1993, ....]
        """
        vals = list()
        for r in self.results:
            for hit in r:
                for k, v in hit.items():
                    vals.append(v)
        return vals


###############################################################################
#
# pref_terms.text2summary
#
###############################################################################
class SummaryReader(Serializable):

    def __init__(self, source):
        self.allergies = list()
        self.medications = list()
        self.problems = list()
        self.labs = list()

        # TODO: This should not be here, feature-service should never import biomed
        # if source:
        #     from biomed.summary import pref_terms
        #     self.from_json(self.init(source, pref_terms.text2summary))

    def from_json(self, source: Dict):
        self.labs = source.get('Lab')
        self.medications = source.get('Medication')
        self.problems = source.get('DiseaseDisorder')
        self.allergies = source.get('Allergy')

    def to_json(self) -> Dict:
        return {'Allergy': self.allergies,
                'Lab': self.labs,
                'DiseaseDisorder': self.problems,
                'Medication': self.medications}
