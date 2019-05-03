import json
import re

from kqml import KQMLString
from .kqml_list import KQMLList
from .kqml_token import KQMLToken
from .kqml_exceptions import KQMLException


def cl_from_json(json_obj):
    """Read a json into a KQMLList object, recursively usng the CLJson paradigm.

    Note: both false an None are mapped to NIL. This means parsing back will
    not have exactly the same result as the original json dict/list, in some
    cases.
    """
    if isinstance(json_obj, str):
        json_obj = json.loads(json_obj)
    elif isinstance(json_obj, bytes):
        json_obj = json.loads(json_obj.decode('utf-8'))
    elif not isinstance(json_obj, list) and not isinstance(json_obj, dict):
        raise ValueError("Input must be a list, dict, or string/bytes json.")
    return _cl_from_json(json_obj)


JSON_TO_CL_PATTS = [
    # Add a * before upper case at the beginning of lines or after an
    # underscore.
    ([re.compile('^([A-Z][a-z])'), re.compile('_([A-Z][a-z])')],
     lambda m: m.group(0).replace(m.group(1), '') + '*'
               + m.group(1).lower()),

    # Replace Upper case not at the beginning or after an underscore.
    ([re.compile('([A-Z][a-z])')], lambda m: '-' + m.group(1).lower()),

    # Replace groups of upper case words with surrounding pluses.
    ([re.compile('([A-Z0-9]+[A-Z0-9_]*[A-Z0-9]*)')],
     lambda m: '+%s+' % m.group(1).lower().replace('_', '-')),

    # Convert some other special underscores to --
    ([re.compile('([a-z])_([a-z0-9\+*])')], '\\1--\\2'),
]


def _key_from_string(key):
    for patts, repl in JSON_TO_CL_PATTS:
        for patt in patts:
            try:
                new_key = patt.sub(repl, key)
            except Exception:
                print("Exeption in key_from_string:", patt.pattern, repl, key)
                raise
            print('FORE:', new_key, patt.findall(key))
            key = new_key
    return key.upper()


def _cl_from_json(json_obj):
    if isinstance(json_obj, list):
        ret = KQMLList()
        for elem in json_obj:
            ret.append(_cl_from_json(elem))
    elif isinstance(json_obj, dict):
        ret = KQMLList()
        for key, val in json_obj.items():
            ret.set(_key_from_string(key), _cl_from_json(val))
    elif isinstance(json_obj, str):
        ret = KQMLString(json_obj)
    elif isinstance(json_obj, bool):
        if json_obj:
            ret = KQMLToken('T')
        else:
            ret = KQMLToken('NIL')
    elif isinstance(json_obj, int) or isinstance(json_obj, float):
        ret = str(json_obj)
    elif json_obj is None:
        return KQMLToken('NIL')
    else:
        raise KQMLException("Unexpected value %s of type %s."
                            % (json_obj, type(json_obj)))
    return ret


def cl_to_json(kqml_list):
    """Recursively convert a KQMLList into a json-style dict/list.

    Note: Because NIL is used as both None and False in lisp, all NIL is
    returned as None, even if the value was intended, or originally, False.
    """
    if not isinstance(kqml_list, KQMLList):
        raise ValueError("Only a KQMLList might be converted into json.")
    return _cl_to_json(kqml_list)


CL_TO_JSON_PATTS = [
    # Replacy -- with _
    (re.compile('(--)'), '_'),

    # Replace *a with A
    (re.compile('\*([a-z])'), lambda m: m.group(1).upper()),

    # Replace +abc-d+ with ABC_D
    (re.compile('\+([a-z0-9-]+)\+'),
     lambda m: m.group(1).upper().replace('-', '_')),

    # Replace foo-bar with fooBar
    (re.compile('-([a-z])'), lambda m: m.group(1).upper())
]


def _string_from_key(s):
    s = s.lower()
    print('BACK:', s)
    for patt, repl in CL_TO_JSON_PATTS:
        new_s = patt.sub(repl, s)
        print('BACK:', new_s, patt.findall(s))
        s = new_s
    return s


def _cl_to_json(kqml_thing):
    if isinstance(kqml_thing, KQMLList):
        # Find all possible keys (things that start with ":")
        possible_keys = re.findall(':([^\s]+)', kqml_thing.to_string())

        # Determine the true keys by checking we can actually get something
        # from them.
        true_key_values = []
        for k in possible_keys:
            val = kqml_thing.get(k)
            if val is not None:
                true_key_values.append((k, val))

        # Extract the return value.
        if len(true_key_values) == len(kqml_thing)/2:
            # It's a dict!
            ret = {}
            for key, val in true_key_values:
                ret[_string_from_key(key)] = _cl_to_json(val)
        elif not len(true_key_values):
            # It's a list!
            ret = []
            for item in kqml_thing:
                ret.append(_cl_to_json(item))
        else:
            # It's not valid for json.
            raise KQMLException("Cannot convert %s into json, neither list "
                                "nor dict." % kqml_thing.to_string())
    elif isinstance(kqml_thing, KQMLToken):
        s = kqml_thing.to_string()
        if s == 'NIL':
            # This could be either false or None. Because None will almost
            # always have the same meaning as False in pep-8 compliant python,
            # but not vice-versa, we choose None.
            ret = None
        elif s == 'T':
            ret = True
        elif s.isdigit():
            ret = int(s)
        elif s.count('.') == 1 and all(seg.isdigit() for seg in s.split('.')):
            ret = float(s)
        else:
            ret = s
    elif isinstance(kqml_thing, KQMLString):
        s = kqml_thing.string_value()
        if s.isdigit():
            ret = int(s)
        elif s.count('.') == 1 and all(seg.isdigit() for seg in s.split('.')):
            ret = float(s)
        else:
            ret = s
    else:
        raise KQMLException("Unexpected value %s of type %s."
                            % (kqml_thing, type(kqml_thing)))
    return ret
