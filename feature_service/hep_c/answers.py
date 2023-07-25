from os.path import basename

from text2phenotype.common import common

from feature_service.resources import HEP_C_SAMPLES, HCV_IGNORE_BSV


class QuestionAnswers:
    """
    BSV Bar Separated Values of "Questions and Answers"

    Answers to HCVPresentationForm questions

        Convenience class for retrieving
        dict: { form questions : concept answers }
    """
    def __init__(self):
        self.ignore = self._load_file(HCV_IGNORE_BSV)
        self.lookup = self._load_once()

    def questions(self):
        """
        Get list of questions that are mapped for this BSV
        :return: list of form keys
        """
        return list(self.lookup.keys())

    def concepts(self, question: str) -> list:
        """
        Get a list of allowable concept CUI for a specific
        question on the HCVPresentationForm

        :param question: 'alcohol_problem'
        :return: list of cui
        """
        concept_dict = self.lookup.get(question, {})
        return list(concept_dict.keys())

    @staticmethod
    def _load_file(filepath_bsv: str) -> list:
        """
        Load 1 bsv sample file into a list of { key=concepts : values=texts }
        :param filepath_bsv: real filepath
        :return: list
        """
        res = list()
        text = common.read_text(filepath_bsv)

        for line in text.splitlines():
            cols = line.split('|')

            if len(cols) > 1:
                cuis = cols[0]
                vals = cols[1:]

                res.append({cuis: vals})

        return res

    def _load_once(self) -> dict:
        """
        Load all of the BSV files from the HEPC_SAMPLE_PATH, ... and only once!
        :return: dict of all BSV where {key:val} is {"hcv_dict.question": concepts }
        """
        res = {}

        for file in common.get_file_list(HEP_C_SAMPLES, '.bsv'):
            if 'ignore' in file:
                continue

            text = common.read_text(file)
            bsv = basename(file).replace('.bsv', '')

            for line in text.splitlines():
                cols = line.split('|')
                if len(cols) <= 1:
                    continue

                cui = cols[0]
                if cui in self.ignore:
                    continue

                bsv_dict = res.setdefault(bsv, {})
                cui_list = bsv_dict.setdefault(cui, [])
                cui_list.extend(cols[1:])

        return res
