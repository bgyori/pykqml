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


def _key_from_string(key):
    patts = [
        # Replace a pair of upper-case words with an underscore. Make
        # lowercase so that they don't get picked up in future searches.
        (['([A-Z0-9]+)_([A-Z0-9]+)'],
         lambda m: '+%s-%s+' % tuple(s.lower() for s in m.groups())),

        # Add a * before upper case at the beginning of lines or after an
        # underscore.
        (['^([A-Z][a-z])', '_([A-Z][a-z])'],
         lambda m: m.group(0).replace(m.group(1), '') + '*'
                   + m.group(1).lower()),

        # Replace Upper case not at the beginning or after an underscore.
        (['([A-Z][a-z])'], lambda m: '-' + m.group(1).lower()),

        # Replace groups of upper case words with surrounding pluses.
        (['([A-Z0-9]{2,})'], lambda m: '+%s+' % m.group(1).lower()),

        # Convert some other special underscores to --
        (['([a-z])_([a-z0-9\+*])'], '\\1--\\2'),
    ]
    for patts, repl in patts:
        for patt in patts:
            try:
                new_key = re.sub(patt, repl, key)
            except Exception:
                print(patt, repl, key)
                raise
            print(new_key, re.findall(patt, key))
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
            ret.set(key, _cl_from_json(val))
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


def _cl_to_json(kqml_thing):
    if isinstance(kqml_thing, KQMLList):
        possible_keys = re.findall(':(\w+)', kqml_thing.to_string())
        true_keys = [k for k in possible_keys if kqml_thing.get(k) is not None]
        if len(true_keys) == len(kqml_thing)/2:
            # It's a dict!
            ret = {}
            for key in true_keys:
                ret[key] = _cl_to_json(kqml_thing.get(key))
        elif not len(true_keys):
            # It's a list!
            ret = []
            for item in kqml_thing:
                ret.append(_cl_to_json(item))
        else:
            # It's not valid for json.
            raise KQMLException("Cannot convert %s into json."
                                % kqml_thing.to_string())
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
