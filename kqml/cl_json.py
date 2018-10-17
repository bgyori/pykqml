from .kqml_string import KQMLString
from .kqml_list import KQMLList
from .kqml_token import KQMLToken
from .kqml_exceptions import KQMLException


def parse_json(json_obj):
    if isinstance(json_obj, list):
        ret = KQMLList()
        for elem in json_obj:
            ret.append(parse_json(elem))
    elif isinstance(json_obj, dict):
        ret = KQMLList()
        for key, val in json_obj.items():
            ret.set(key, parse_json(val))
    elif isinstance(json_obj, str):
        ret = KQMLString(json_obj)
    elif isinstance(json_obj, bool):
        if json_obj:
            ret = KQMLToken('T')
        else:
            ret = KQMLToken('NIL')
    elif isinstance(json_obj, int) or isinstance(json_obj, float):
        ret = KQMLString(str(json_obj))
    elif json_obj is None:
        return KQMLToken('NIL')
    else:
        raise KQMLException("Unexpected value %s of type %s."
                            % (json_obj, type(json_obj)))
    return ret
