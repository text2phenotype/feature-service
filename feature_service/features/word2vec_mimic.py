from text2phenotype.constants.features import FeatureType
from feature_service.features.feature import Feature



class Word2VecMimic(Feature):
    feature_type = FeatureType.word2vec_mimic
    vector_length = 128
    annotated_feature = 'token'
    requires_annotation = False

    def vectorize_token(self, token, **kwargs):
        if token.lower() in self.Feature_Cache.word2vec_mimic():
            unparsed_embedding = self.Feature_Cache.word2vec_mimic()[token.lower()].split()
        else:
            unparsed_embedding = self.Feature_Cache.word2vec_mimic()['UNK'].split()
        # weird format from embedding output, parse it accordingly
        word_emb = []
        if unparsed_embedding[0] != '[' and '[' in unparsed_embedding[0]:
            # some embedding has the first floating number starting with '[' or is '[' due to formatting issue
            word_emb.append(float(unparsed_embedding[0][1:]))
        for j in range(1, len(unparsed_embedding) - 1):
            word_emb.append(float(unparsed_embedding[j]))
        if unparsed_embedding[-1] != ']' and ']' in unparsed_embedding[-1]:
            # some embedding has the last floating number ending with ']' or is ']' due to some formatting issue
            word_emb.append(float(unparsed_embedding[-1][:-1]))
        vector = word_emb

        return vector
