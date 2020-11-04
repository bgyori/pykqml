from io import BytesIO
from kqml import KQMLObject
from . import kqml_reader
from . import kqml_list
from .kqml_token import KQMLToken
from .kqml_exceptions import KQMLBadPerformativeException
from .util import safe_decode, safe_encode


class KQMLPerformative(KQMLObject):
    def __init__(self, objects):
        if not objects:
            raise KQMLBadPerformativeException('no elements for initialization')
        # If we get a string then we start a list with the string as the head
        if isinstance(objects, str):
            self.data = kqml_list.KQMLList(objects)
        elif isinstance(objects, kqml_list.KQMLList):
            self._validate(objects)
            self.data = objects

    @staticmethod
    def _validate(objects):
        if not isinstance(objects[0], KQMLToken):
            raise KQMLBadPerformativeException('list doesn\'t start ' +
                'with KQMLToken: ' + str(objects[0]))
        i = 1
        while i < len(objects):
            if not isinstance(objects[i], KQMLToken) or objects[i][0] != ':':
                raise KQMLBadPerformativeException('performative ' +
                    'element not a keyword: ' + str(objects[i]))
            # Increment counter after keyword
            i += 1
            if i == len(objects):
                raise KQMLBadPerformativeException('missing value ' +
                    'for keyword: ' + str(objects[i-1]))
            i += 1

    def __len__(self):
        return len(self.data)

    def head(self):
        return self.data.head()

    def get(self, keyword):
        return self.data.get(keyword)

    def gets(self, keyword):
        return self.data.gets(keyword)

    def set(self, keyword, value):
        self.data.set(keyword, value)

    def sets(self, keyword, value):
        self.data.sets(keyword, value)

    def to_list(self):
        return self.data

    def write(self, out):
        self.data.write(out)

    def to_string(self):
        return safe_decode(self.data.to_string())

    @classmethod
    def from_string(cls, s):
        s = safe_encode(s)
        sreader = BytesIO(s)
        kreader = kqml_reader.KQMLReader(sreader)
        return cls(kreader.read_list())

    def __str__(self):
        return safe_decode(self.to_string())

    def __repr__(self):
        return self.data.__repr__()
