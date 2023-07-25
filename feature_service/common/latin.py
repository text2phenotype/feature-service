import string
import enum


class Latin:

    def __init__(self, **kwargs):
        """
        :param kwargs:
        pre "PREFIX" like 'supra'
        suf "SUFFIX" like 'icle'
        ftr "FEATURE" like Position ( anatomic position )
        eng "ENGLISH" is the translation, like 'above'
        test "EXAMPLE" is an example of the latin prefix/suffix, such as 'surpra'
        desc "list of ENGLISH" words, optional
        """
        self.ftr = kwargs.get('ftr', None)
        self.eng = kwargs.get('eng', None)
        self.pre = kwargs.get('pre', None)
        self.suf = kwargs.get('suf', None)
        self.test = kwargs.get('test', None)
        self.desc = kwargs.get('desc', None)

        if self.pre and self.suf:
            if len(self.pre) > 0 and len(self.suf) > 0:
                raise Exception(f"prefix '{self.pre}' and suffix '{self.suf}' should not both be set")
        elif self.is_prefix():
            self.latin = self.pre
        elif self.is_suffix():
            self.latin = self.suf

    def match(self, token: str, latin_case=None) -> bool:
        """
        :param token: alphabetical word
        :param latin_case: case sensitivity
        :return: bool True if token.isalpha() and token is "string in string" in self.latin else False
        """
        token = token.translate(str.maketrans('', '', string.punctuation))

        if not token.isalpha():
            return False

        latin_case = latin_case if latin_case else self.latin

        if latin_case is None:
            raise Exception(f'unexpected null? {self.__dict__}')

        if len(latin_case) >= len(token):
            return False

        if self.is_prefix():
            return token.startswith(latin_case)

        if self.is_suffix():
            return token.endswith(latin_case)

    def relax(self, token: str) -> bool:
        """
        :param token:
        :return: case insensitive match ( relax )
        """
        return self.match(token.lower(), self.latin.lower())

    def strict(self, token: str) -> bool:
        """
        :param token:
        :return: case dependent match ( strict )
        """
        return self.match(token, self.latin)

    def title(self, token: str) -> bool:
        """
        :param token:
        :return: title case match, especially for beginning of sentence or section header ( Title )
        """
        return self.match(token, self.latin.title())

    def upper(self, token: str) -> bool:
        """
        :param token:
        :return: uppercase match, especially for section header ( UPPER )
        """
        return self.match(token, self.latin.upper())

    def is_prefix(self, min_chars=1) -> bool:
        return self.pre is not None and len(self.pre) >= min_chars

    def is_suffix(self, min_chars=1) -> bool:
        return self.suf is not None and len(self.suf) >= min_chars

    def is_valid(self) -> bool:
        return self.match(self.test)

    def __str__(self):
        return self.latin


class LatinTypes(enum.IntEnum):
    anatomy = 0
    color = 1
    condition = 2
    general = 3
    pertainingto = 4
    position = 5
    procedure = 6
    quantity = 7
