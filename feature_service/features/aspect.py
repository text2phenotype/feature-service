from abc import ABC
from collections import defaultdict

from text2phenotype.ccda.section import Aspect as AspectEnum
from text2phenotype.constants.features import FeatureType

from feature_service.aspect.chunker import Chunker
from feature_service.features.feature import Feature


class Aspect(Feature, ABC):
    feature_type = FeatureType.aspect
    vector_length = len(AspectEnum.__members__)

    def annotate(self, text: str, **kwargs):
        """
        :param text: run chunker and get a list() of positions
        :return: list [ dict keys{range, aspect, text} ]
        """
        chunker = Chunker()
        positions = chunker.predict_aspect_emb_by_section_no_enforce(text)
        matches = defaultdict(list)
        for line in positions:
            if line[self.feature_type.name] is not None:
                matches[line['range']].append(line[self.feature_type.name])

        return matches.items()

    def vectorize_token(self, token, **kwargs) -> list:
        vector = self.default_vector.copy()
        vector[AspectEnum[token[0]].value] = 1
        return vector


class AspectEnforce(Aspect):
    feature_type = FeatureType.aspect_enforce

    def annotate(self, text: str, **kwargs):
        """
        :param text: run chunker and get a list() of positions
        :return: list [ dict keys{range, aspect, text} ]
        """
        chunker = Chunker()
        positions = chunker.return_aspect_emb_section_positions_enforce(text)
        matches = defaultdict(list)
        for line in positions:
            if line['aspect'] is not None:
                matches[line['range']].append(line['aspect'])
        return matches.items()


class AspectLine(Aspect):
    feature_type = FeatureType.aspect_line

    def annotate(self, text: str, **kwargs):
        """
        :param text: run chunker and get a list() of positions
        :return: list [ dict keys{range, aspect, text} ]
        """
        chunker = Chunker()
        positions = chunker.predict_aspect_emb_by_line(text)
        matches = defaultdict(list)
        for line in positions:
            if line['aspect'] is not None:
                matches[line['range']].append(line['aspect'])
        return matches.items()
