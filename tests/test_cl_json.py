from kqml import cl_json, KQMLList


def test_parse():
    json_dict = {'a': 1, 'b': 2,
                 'c': ['foo', {'bar': None, 'done': False}],
                 'this_is_json': True}
    res = cl_json._cl_from_json(json_dict)
    assert isinstance(res, KQMLList)
    assert len(res) == 2*len(json_dict.keys())
    back_dict = cl_json.cl_to_json(res)
    assert len(back_dict) == len(json_dict)
    # TODO: Should test for equality.
