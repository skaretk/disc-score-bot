
class Course:
    def __init__(self, name):
        self._name = name
        self._layout = None
        self._url = ""

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, layout):
        self._layout = layout

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url
