import StringIO
from kqml_token import KQMLToken
import kqml_reader

class KQMLList(object):
    def __init__(self, objects=None):
        self.data = []
        # If no objects are passed, we start with an empty list
        if objects is None:
            objects = []
        # If a list is passed, the elements are one-by-one added to the list
        if isinstance(objects, list):
            for o in objects:
                self.append(o)
        # If a string is passed, it becomes the "head" of the list
        elif isinstance(objects, basestring):
            self.append(objects)

    def __str__(self):
        return '(' + ' '.join([d.__str__() for d in self.data]) + ')'

    def __repr__(self):
        return '(' + ' '.join([d.__repr__() for d in self.data]) + ')'

    def __getitem__(self, *args):
        return self.data.__getitem__(*args)

    def __len__(self):
        return len(self.data)

    def append(self, obj):
        if isinstance(obj, basestring):
            self.data.append(KQMLToken(obj))
        else:
            self.data.append(obj)

    def push(self, obj):
        self.data.insert(0, obj)

    def insert_at(self, index, obj):
        self.data.insert(index, obj)

    def remove_at(self, index):
        del self.data[index]

    def nth(self, n):
        return self.data[n]

    def head(self):
        return self.data[0].to_string()

    def get(self, keyword):
        if not keyword.startswith(':'):
            keyword = ':' + keyword
        for i, s in enumerate(self.data):
            if s.to_string().upper() == keyword.upper():
                if i < len(self.data)-1:
                    return self.data[i+1]
                else:
                    return None
        return None

    def gets(self, keyword):
        param = self.get(keyword)
        if param:
            return param.to_string()
        return None

    def set(self, keyword, value):
        if not keyword.startswith(':'):
            keyword = ':' + keyword
        found = False
        for i, key in enumerate(self.data):
            if key.to_string().lower() == keyword.lower():
                found = True
                if i < len(self.data)-1:
                    self.data[i+1] = value
                break
        if not found:
            self.data.append(keyword)
            self.data.append(value)

    def write(self, out):
        full_str = '(' + ' '.join([str(s) for s in self.data]) + ')'
        out.write(full_str)

    def to_string(self):
        out = StringIO.StringIO()
        self.write(out)
        return out.getvalue()

    @classmethod
    def from_string(cls, s):
        sreader = StringIO.StringIO(s)
        kreader = kqml_reader.KQMLReader(sreader)
        return kreader.read_list()

    def sublist(self, from_idx, to_idx=None):
        if to_idx is None:
            to_idx = len(self)
        return KQMLList(self.data[from_idx:to_idx])

    def index_of(self, obj):
        if isinstance(obj, basestring):
            return self.index_of_string(obj)
        else:
            try:
                idx = self.data.index(obj)
                return idx
            except ValueError:
                return -1

    def index_of_ignore_cae(self, keyword):
        for i, s in enumerate(self.data):
            if s.lower() == keyword.lower():
                return i
        return -1

    # TODO: check if java indexOf return values are consistent
    def index_of_string(self, s):
        try:
            idx = self.data.index(s)
            return idx
        except ValueError:
            return -1


    #TODO: didn't implement all the functions here
