import sys
from six import BytesIO, StringIO, string_types
from kqml.kqml_reader import KQMLReader
from kqml.kqml_list import KQMLList
import unittest

class TestKQMLReader(unittest.TestCase):
    def test_read_list(self):
        s = '(FAILURE :reason INVALID_DESCRIPTION)'
        # str -> bytes
        sreader = BytesIO(s.encode("utf-8"))
        kr = KQMLReader(sreader)
        lst = kr.read_list()
        for obj in lst:
            assert(not(isinstance(obj, string_types)))

    def test_read_performative(self):
        s = '(REQUEST :CONTENT (REQUEST_TYPE :CONTENT "<ekb>ONT::PROTEIN</ekb>"))'
        # str -> bytes
        sreader = BytesIO(s.encode("utf-8"))
        kr = KQMLReader(sreader)
        kp = kr.read_performative()
