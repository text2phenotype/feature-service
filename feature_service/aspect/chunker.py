import string

from text2phenotype.ccda.section import Aspect

from feature_service.feature_set.feature_cache import FeatureCache


class Chunker:
    def __init__(self):
        cache = FeatureCache()
        self.vectorizer = cache.aspect_vectorizer()
        self.vocabulary = cache.aspect_vocabulary()
        self.classifier = cache.aspect_classifier()
        self.aspect_class = 7  # << 'Aspect.' is a seven character long string

    def predict_aspect(self, text, confidence_threshold: float = 0):
        """
        :param text: string, the piece of text that we want to chunker
        :return: predicted aspect for the piece of text
        """
        annotated = text
        text_feature = self.vectorizer.transform([annotated])
        predicted_label = self.classifier.predict(text_feature)

        predicted_probability = self.classifier.predict_proba(text_feature)
        if predicted_probability[0][predicted_label[0]] > confidence_threshold:
            aspect = Aspect(predicted_label[0]).name
        else:
            aspect = None

        return aspect, predicted_probability[0][predicted_label[0]], predicted_probability[0]

    def predict_aspect_emb_by_line(self, text):
        """
        :param text: piece of text in emr that we wanted to parse and predict
        """
        content = []
        cursor = 0

        text_list = text.split('\n')
        section_content = ''
        aspect_map = FeatureCache().aspect_map()
        for line in text_list:
            if ':' in line:
                original_line = line.split(':')[0]
                header_to_check = (''.join(c for c in original_line if c not in string.punctuation and
                                           not c.isdigit()).strip()).upper()
                if header_to_check in aspect_map:
                    _aspect = aspect_map[header_to_check][self.aspect_class:]
                    text_range = self.find_range(text, original_line, cursor)
                    line_dict = self.return_line_dict(original_line, True, _aspect, text_range, False)
                else:
                    # TODO: should we keep this line together to make a prediction if the string before ':' is not a
                    #  header?
                    text_range = self.find_range(text, original_line, cursor)
                    line_dict = self.return_line_dict(original_line, False, None, text_range, False)
                content.append(line_dict)
                cursor += (len(original_line) + 1)
                section_content += (':'.join(line.split(':')[1:]) + '\n')
                if section_content:
                    text_range = self.find_range(text, section_content[:-1], cursor)
                    line_dict = self.return_line_dict(section_content[:-1], False, None, text_range, False)
                    content.append(line_dict)
                    cursor += len(section_content)
                    section_content = ''
            elif line.isupper():
                header_to_check = ''.join(c for c in line if c not in string.punctuation and not c.isdigit()).strip()
                header_to_check = header_to_check.upper()
                if header_to_check in aspect_map:
                    _aspect = aspect_map[header_to_check][self.aspect_class:]
                    text_range = self.find_range(text, line, cursor)
                    line_dict = self.return_line_dict(line, True, _aspect, text_range, False)
                else:
                    text_range = self.find_range(text, line, cursor)
                    line_dict = self.return_line_dict(line, False, None, text_range, False)
                content.append(line_dict)
                cursor += (len(line) + 1)
            else:
                if line.strip().upper() in aspect_map:
                    _aspect = aspect_map[line.strip().upper()][self.aspect_class:]
                    text_range = self.find_range(text, line, cursor)
                    line_dict = self.return_line_dict(line, True, _aspect, text_range, False)

                else:
                    text_range = self.find_range(text, line, cursor)
                    line_dict = self.return_line_dict(line, False, None, text_range, False)
                content.append(line_dict)
                cursor += (len(line) + 1)
        return content

    def return_aspect_emb_section_positions_enforce(self, text):
        """
        this function returns aspects parsed by section and also the start/end position of the aspects
        """
        content = []
        predicted = []
        cursor = 0
        text_list = text.split('\n')

        section_content = ''
        _last_aspect = ''
        aspect_map = FeatureCache().aspect_map()
        for line in text_list:
            # if this line contains a ':', take the first part as section heading and second part as content
            if ':' in line:
                original_line = line.split(':')[0]
                # get rid of number and punctuation of this heading
                # TODO: questionable line - what if there is punctuation in the known header already:
                #  such as HOMELESS,ETC. ...
                header_to_check = ("".join(
                    c for c in original_line if c not in string.punctuation and not c.isdigit()).strip()).upper()
                # header_to_check = potential_header
                # uppercase the section heading
                # Get the aspect of this section_heading added to the aspect_list
                if header_to_check in aspect_map:
                    # if in the mapping, know its aspect, directly look up, and take the second part to the classifer
                    if section_content:
                        # if section content is not empty, assign it an aspect,
                        if _last_aspect:
                            # if _last_aspect is not empty, then assign last aspect to the current content
                            predicted.append(_last_aspect)
                            text_range = self.find_range(text, section_content, cursor)
                            line_dict = self.return_line_dict(section_content, False, None, text_range, False)
                            line_dict['aspect'] = _last_aspect
                            # re-assign the section content to be empty

                        else:
                            # if last_aspect is empty then use predict_aspect to assign an aspect to the section content
                            # predicted.append(predict_aspect(section_content, classifier)[0])
                            text_range = self.find_range(text, section_content, cursor)
                            line_dict = self.return_line_dict(section_content, False, None, text_range, False)
                        content.append(line_dict)
                        cursor += len(section_content)
                        section_content = ''

                    predicted.append(aspect_map[header_to_check][self.aspect_class:])
                    _aspect = aspect_map[header_to_check][self.aspect_class:]
                    text_range = self.find_range(text, original_line, cursor)
                    line_dict = self.return_line_dict(original_line, True, _aspect, text_range, False)
                    content.append(line_dict)
                    cursor += (len(original_line) + 1)
                    _last_aspect = aspect_map[header_to_check][self.aspect_class:]
                    section_content += (':'.join(line.split(':')[1:]) + '\n')
                else:
                    section_content += (line + '\n')

            # else check if this line is all uppercase, if it is, it's a section heading in practice fusion case, but
            # not necessarily
            elif line.isupper():
                # convert the header format, prepare to look up
                # TODO: questionable line, maybe don't have to get rid of punctuation or numbers inside the line
                header_to_check = (
                    ''.join(c for c in line if c not in string.punctuation and not c.isdigit()).strip()).upper()
                # header_to_check = potential_header
                if header_to_check in aspect_map:
                    # if the header is in the map, then know its aspect
                    # this part deal with potential last section content
                    if section_content:
                        # if section content is not empty, assign it an aspect,
                        if _last_aspect:
                            # if _last_aspect is not empty, then assign last aspect to the current content
                            predicted.append(_last_aspect)
                            text_range = self.find_range(text, section_content, cursor)
                            line_dict = self.return_line_dict(section_content, False, None, text_range, False)
                            line_dict['aspect'] = _last_aspect

                        else:
                            # if last_aspect is empty then use predict_aspect to assign an aspect to the section content
                            predicted.append(self.predict_aspect(section_content)[0])
                            text_range = self.find_range(text, section_content, cursor)
                            line_dict = self.return_line_dict(section_content, False, None, text_range, False)
                        content.append(line_dict)
                        cursor += len(section_content)
                        section_content = ''
                    # then assign the aspect from the gold mapping to the header
                    predicted.append(aspect_map[header_to_check][self.aspect_class:])
                    _aspect = aspect_map[header_to_check][self.aspect_class:]
                    text_range = self.find_range(text, line, cursor)
                    line_dict = self.return_line_dict(line, True, _aspect, text_range, False)
                    content.append(line_dict)
                    cursor += len(line)
                    _last_aspect = aspect_map[header_to_check][self.aspect_class:]
                else:
                    section_content += (line + '\n')
            else:
                # if this line is not a potential header line try see if this line is in the mappings, if it is, then
                # it's a header format that falls in neither of the two categories and then write its aspect and line in
                # the file
                # maybe should get rid of the numbers and punctuations as well(?), should catch problems
                if line.upper().strip() in aspect_map:
                    # deal with potential section content
                    if section_content:
                        # if section content is not empty, assign it an aspect,
                        if _last_aspect:
                            # if _last_aspect is not empty, then assign last aspect to the current content
                            text_range = self.find_range(text, section_content, cursor)
                            line_dict = self.return_line_dict(section_content, False, None, text_range, False)
                            line_dict['aspect'] = _last_aspect

                        else:
                            # if last_aspect is empty then use predict_aspect to assign an aspect to the section content
                            text_range = self.find_range(text, section_content, cursor)
                            line_dict = self.return_line_dict(section_content, False, None, text_range, False)
                        content.append(line_dict)
                        cursor += len(section_content)
                        section_content = ''

                    _aspect = aspect_map[line.upper().strip()][self.aspect_class:]
                    text_range = self.find_range(text, line, cursor)
                    line_dict = self.return_line_dict(line, True, _aspect, text_range, False)
                    content.append(line_dict)
                    cursor += len(line)
                    _last_aspect = aspect_map[line.upper().strip()][self.aspect_class:]
                else:
                    section_content += (line + '\n')

        # if there is left over section content to be assigned
        if section_content:
            if _last_aspect:
                # if _last_aspect is not empty, then assign last aspect to the current content
                text_range = self.find_range(text, section_content[:-1], cursor)
                line_dict = self.return_line_dict(section_content[:-1], False, None, text_range, False)
                line_dict['aspect'] = _last_aspect

            else:
                # if _last_aspect is empty, then use predict_aspect to assign an aspect to the section content
                text_range = self.find_range(text, section_content[:-1], cursor)
                line_dict = self.return_line_dict(section_content[:-1], False, None, text_range, False)
            content.append(line_dict)
            cursor += len(section_content)
            section_content = ''

        return content

    def predict_aspect_emb_by_section_no_enforce(self, text):
        """
        logic: first see if any of the line/heading in the mapping, and then if the line is not in the mapping, run
        sectionizer to predict an aspect for the line.
        refer to the i2b2_txt_parser code
        For practice fusion data, recognize a section heading by checking if the line is all Capitalized
        For centricity data, check if there is ':' in the line, if there is, get the string before the ':' as section
        heading and check if the heading is in the mapping, otherwise, predict an aspect for the heading, take the
        string after the ':' and concatenate with any string before the next line that contains with ':'
        Another rule - always look up the line if the line is in the section_aspect.json mapping, this means that if the
        line neither contains ':' nor are all uppercase, we should look it up in the mapping, and assign a aspect to it
        accordingly
        takes in a piece of text and return a sequence of tags, examples are practice fusion fake record and centricity
        fake record
        :param text: the content of an emr file
        :return: list aspects tagged either by the classifier or the section_aspect_mapping
        """
        content = []  # result, list of dictionaries
        predicted = []
        cursor = 0

        section_content = ''
        aspect_map = FeatureCache().aspect_map()
        for line in text.splitlines():
            # if this line contains a ':', take the first part as section heading and second part as content
            if ':' in line:
                # TODO: should we only append the section content after we know that we meet a header?
                # if the previous section_content is not empty, since we meet a new seciton here, chunker it and reset
                # section_content to empty string
                if section_content:
                    text_range = self.find_range(text, section_content, cursor)

                    content.append(self.return_line_dict(section_content, False, None, text_range, False))

                    cursor += len(section_content)
                    section_content = ''
                # take out the string before ':'
                original_line = line.split(':')[0]
                # get rid of number and punctuation of this heading
                # TODO: questionable line - what if there is punctuation in the known header already: such as
                #  HOMELESS,ETC. ...
                header_to_check = ("".join(
                    c for c in original_line if c not in string.punctuation and not c.isdigit()).strip()).upper()

                # Get the aspect of this section_heading added to the aspect_list
                # steps:
                # 1. if in the mapping, good, know its aspect, directly look up, and take the second part to the
                # classifer
                # 2. if not in the mapping, use classifier to chunker the whole line to be one aspect
                if header_to_check in aspect_map:
                    predicted.append(aspect_map[header_to_check][self.aspect_class:])
                    _aspect = aspect_map[header_to_check][self.aspect_class:]
                    text_range = self.find_range(text, original_line, cursor)
                    # line_dict = return_line_dict(original_line, True, _aspect, range, False)
                    content.append(self.return_line_dict(original_line, True, _aspect, text_range, False))
                    cursor += (len(original_line) + 1)
                    # get the string after the ':' as the potentially part the the section_content.
                    section_content = ':'.join(line.split(':')[1:]) + '\n'
                else:
                    section_content += (line + '\n')

            # else check if this line is all uppercase, if it is, it's a section heading in practice fusion.
            elif line.isupper():
                # TODO: should we only append the section content after we know that we meet a header?
                if section_content:
                    predicted.append(self.predict_aspect(section_content)[0])
                    text_range = self.find_range(text, section_content, cursor)
                    content.append(self.return_line_dict(section_content, False, None, text_range, False))
                    cursor += len(section_content)
                    section_content = ''
                # convert the header format, prepare to look up
                # TODO: questionable line, maybe don't have to get rid of punctuation or numbers inside the line
                header_to_check = (
                    ''.join(c for c in line if c not in string.punctuation and not c.isdigit()).strip()).upper()
                # header_to_check = potential_header
                if header_to_check in aspect_map:
                    predicted.append(aspect_map[header_to_check][self.aspect_class:])
                    _aspect = aspect_map[header_to_check][self.aspect_class:]
                    text_range = self.find_range(text, line, cursor)
                    content.append(self.return_line_dict(line, True, _aspect, text_range, False))
                    cursor += len(line)
                else:
                    section_content += (line + '\n')
            else:
                # try see if this line is in the mappings, if it is, then it's a header that falls in neither of the two
                # categories and then write its aspect and line in the file
                # maybe should get rid of the numbers and punctuations as well, should catch problems
                if line.upper().strip() in aspect_map:
                    if section_content:
                        predicted.append(self.predict_aspect(section_content)[0])
                        text_range = self.find_range(text, section_content, cursor)
                        content.append(self.return_line_dict(section_content, False, None, text_range, False))
                        cursor += len(section_content)
                        section_content = ''

                    predicted.append(aspect_map[line.upper().strip()][self.aspect_class:])
                    _aspect = aspect_map[line.upper().strip()][self.aspect_class:]
                    text_range = self.find_range(text, line, cursor)
                    line_dict = self.return_line_dict(line, True, _aspect, text_range, False)
                    content.append(line_dict)
                    cursor += len(line)

                else:
                    section_content += (line + '\n')

        if section_content and section_content not in set([char for char in string.punctuation] + ['\n']):
            text_range = self.find_range(text, section_content[:-1], cursor)
            _line_dict = self.return_line_dict(section_content[:-1], False, None, text_range, False)

            content.append(_line_dict)
            cursor += len(section_content)
            section_content = ''

        return content

    @staticmethod
    def find_range(text, chunk, cursor):
        """
        find the positions of the chunk in this text
        :return: a tuple of (chunk, start_index, end_index)
        """
        start_index = max(text.find(chunk, cursor), cursor)
        end_index = start_index + len(chunk)
        return start_index, end_index

    def return_line_dict(self, text, header, aspect, text_range, aspect_emb):
        """
        :param text:
        :param header: boolean, True or False
        :param aspect_emb: True or False, whether we add aspect embedding or not
        :return: a dictionary for the text
        """

        line_dict = {'range': text_range, 'text': text}
        if aspect:
            line_dict['direct_match'] = 1

        if header:
            line_dict['header'] = True
            line_dict['aspect'] = aspect

        else:
            line_dict['header'] = False
            line_dict['aspect'] = self.predict_aspect(text, confidence_threshold=.75)[0]

        if aspect_emb:
            prob_vec = self.predict_aspect(text, confidence_threshold=.75)[2]
            # TODO: JIRA/BIOMED-246
            aspect_prob = {}
            i = 0
            for k in Aspect.get_active_aspects():
                aspect_prob[k.name] = round(float(prob_vec[i]), 3)
                if i < (len(prob_vec) - 1):
                    i = i + 1
                else:
                    break
            aspect_prob['device'] = 0.0
            aspect_prob['other'] = 0.0

            line_dict['aspect_prob'] = aspect_prob

        return line_dict
