from bs4 import BeautifulSoup
from bs4.element import NavigableString


class SEObject(object):
    """
    Base Object for SE Objects
    """
    def __init__(self, data):
        self._data = data


class User(SEObject):
    """
    Stack Overflow User object which will hold information for use in
    Nidaba analysis.
    """

    def __init__(self, data):
        """
        :param data: dict containing user information.
        :return: None
        """
        super().__init__(data)


class Post(SEObject):
    """
    Base object for Question, Answer, Comments
    """

    def __init__(self, data):
        """
        :param data: Dict containing comment information.
        :return: None
        """
        super().__init__(data)
        self.body = self._data.get('Body', '')
        self.text = self._get_text(self.body)
        self.code = self._get_code(self.body)

    @classmethod
    def _get_code(cls, html):
        return [i.get_text() for i in BeautifulSoup(html).find_all('code')]

    @classmethod
    def _get_text(cls, html):
        soup = BeautifulSoup(html)
        [s.extract() for s in soup('code')]
        return [i for i in soup.recursiveChildGenerator()
                if isinstance(i, NavigableString)]


class Comment(Post):
    """
    Stack Overflow Comment object which will hold information for use in
    Nidaba analysis.
    """

    def __init__(self, data):
        """
        :param data: Dict containing comment information.
        :return: None
        """
        super().__init__(data)


class Answer(Post):
    """
    Stack Overflow Answer object which will hold information for use in
    Nidaba analysis.
    """

    def __init__(self, data):
        """
        :param data: dict containing answer information.
        :return: None
        """
        super().__init__(data)


class Question(Post):
    """
    Stack Overflow Question object which will hold information for use in
    Nidaba analysis.
    """

    def __init__(self, data, answers=None, comments=None):
        """
        :param data: Dict containing question information.
        :param answers: List of dicts containing answer information.
        :param comments: List of dicts containing comment information
        :return: None
        """
        super().__init__(data)

        if answers is None:
            self.answers = []
        else:
            self.answers = [Answer(ans) for ans in answers]

        if comments is None:
            self.comments = []
        else:
            self.comments = [Comment(comm) for comm in comments]