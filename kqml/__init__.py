__version__ = '0.4'
import logging

class KQMLObject(object):
    """This is the parent class for KQML classes representing messages."""
    pass

from kqml_exceptions import *
from kqml_quotation import KQMLQuotation
from kqml_token import KQMLToken
from kqml_string import KQMLString
from kqml_list import KQMLList
from kqml_performative import KQMLPerformative
from kqml_reader import KQMLReader
from kqml_dispatcher import KQMLDispatcher
from kqml_module import KQMLModule

logging.basicConfig(format='%(levelname)s: %(modulename)s/%(name)s - %(message)s',
                    level=logging.INFO)
