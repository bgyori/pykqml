from kqml import cl_json, KQMLList


def test_parse():
    json_dict = {'a': 1, 'b': 2,
                 'c': ['foo', {'bar': None, 'done': False}],
                 'this is json': True}
    res = cl_json.parse_json(json_dict)
    assert isinstance(res, KQMLList)
    assert len(res) == 2*len(json_dict.keys())
