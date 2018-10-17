import json
import re

from .kqml_string import KQMLString
from .kqml_list import KQMLList
from .kqml_token import KQMLToken
from .kqml_exceptions import KQMLException


def cl_from_json(json_obj):
    if isinstance(json_obj, str):
        json_obj = json.loads(json_obj)
    elif isinstance(json_obj, bytes):
        json_obj = json.loads(json_obj.decode('utf-8'))
    elif not isinstance(json_obj, list) and not isinstance(json_obj, dict):
        raise ValueError("Input must be a list, dict, or string/bytes json.")
    return _cl_from_json(json_obj)


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
        ret = KQMLToken(json_obj)
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
    else:
        raise KQMLException("Unexpected value %s of type %s."
                            % (kqml_thing, type(kqml_thing)))
    return ret
