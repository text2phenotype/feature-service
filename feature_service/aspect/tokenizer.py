import string


# TODO: JIRA/BIOMED-198


class Tokenizer:
    def __init__(self, stop_words: list):
        self.stop_words = stop_words

    def __call__(self, utterance):
        """
        This function takes in a single text (just the text part)
        then it will process/clean the text and return a list of tokens (words).
        For example, if text was 'I eat', the function returns ['i', 'eat']

        You will not need to call this function explicitly.
        Once you initialize your vectorizer with this tokenizer,
        then 'vectorizer.fit_transform()' will implicitly call this function to
        extract features from the training set, which is a list of tweet texts.
        So once you call 'fit_transform()', the '__call__' function will be applied
        on each tweet text in the training set (a list of tweet texts),

        :param utterance: piece of text, may or may not be a paragraph, complete sentence, or sentence fragment, etc.
        :return: list of word features
        """
        features = []

        # tweet.lower().strip()
        # print tweet
        utterance.lower().strip()

        # punct is a set of punctuations
        punct = set(string.punctuation) - {'_', '$', '/', '-'}

        # replace all punctuations with space
        for char in punct:
            utterance = utterance.replace(char, ' ')

        words = utterance.split()
        # split the word into list of tokens

        # further cleaning of the tokens with rules applied.
        for word in words:
            # if the first character is not a alphabetic character, then continue to next word.
            # if not word[0].isalpha():
            # if the first character is not a alphabetic character, check the if the word
            # is a zipcode, if it is, then replace it with "zipcode"
            # if word.isdigit() and len(word) == 5:
            #    # print word
            #    word = "zip_code"
            #    # if the word is a name, change the token to patient, family name.
            # elif word in self.name_list:
            #    word = "patient_name"
            # elif word in self.hospital_list:
            #    word = "hospital"
            # else:
            #    continue
            if word in self.stop_words:
                continue

                # apply stemming to the token
            features.append(word)

        return features
