from kqml import cl_json, KQMLList


def _equal(json_val, back_json_val):
    if json_val is False and back_json_val is None:
        return True
    if type(json_val) != type(back_json_val):
        print("Mismatched type:", type(json_val), type(back_json_val))
        return False

    if isinstance(json_val, dict):
        ret = True
        for key, value in json_val.items():
            if not _equal(value, back_json_val[key]):
                print("Dict at %s:" % key, value, back_json_val[key])
                ret = False
                break
    elif isinstance(json_val, list):
        ret = True
        for i, value in enumerate(json_val):
            if not _equal(value, back_json_val[i]):
                print("List at %s:" % i, value, back_json_val[i])
                ret = False
                break
    else:
        ret = (json_val == back_json_val)
        if not ret:
            print("Values not equal:", json_val, back_json_val)
    return ret


def test_simple_parse():
    json_dict = {'a': 1, 'b': 2,
                 'c': ['foo', {'bar': None, 'done': False}],
                 'this_is_json': True}
    res = cl_json._cl_from_json(json_dict)
    print(res.to_string())
    assert isinstance(res, KQMLList)
    assert len(res) == 2*len(json_dict.keys())
    back_dict = cl_json.cl_to_json(res)
    assert len(back_dict) == len(json_dict)
    assert _equal(json_dict, back_dict)


def test_more_complex_parse():
    json_dict = {'a': 1, 'B': 2,
                 'c': ['f oo -', {'bar': None, 'done': False}],
                 'This is-Json': True}
    res = cl_json._cl_from_json(json_dict)
    print(res.to_string())
    assert isinstance(res, KQMLList)
    assert len(res) == 2*len(json_dict.keys())
    back_dict = cl_json.cl_to_json(res)
    assert len(back_dict) == len(json_dict)
    assert _equal(json_dict, back_dict)
