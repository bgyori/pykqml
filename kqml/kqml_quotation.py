import StringIO
from kqml import KQMLObject

class KQMLQuotation(KQMLObject):
    def __init__(self, quote_type, kqml_object):
        self.quote_type = quote_type
        self.kqml_object = kqml_object

    def get_type(self):
        return self.quote_type

    def get_object(self):
        return self.kqml_object

    def write(self, out):
        out.write(self.quote_type)
        self.kqml_object.write(out)

    def to_string(self):
        out = StringIO.StringIO()
        self.write(out)
        return out.getvalue()
