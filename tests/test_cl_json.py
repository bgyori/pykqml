import sys

from kqml import cl_json, KQMLList
from kqml.cl_json import CLJsonConverter


def _equal(json_val, back_json_val, strict=False):
    # This handles the case where False->NIL which is not reliably
    # back-translated.
    if not strict:
        if json_val is False and back_json_val is None:
            return True

    # Make sure the types are the same.
    if type(json_val) != type(back_json_val):
        print("Mismatched type:", type(json_val), type(back_json_val))
        return False

    # Check for equalities of values (recursively)
    if isinstance(json_val, dict):
        ret = True
        for key, value in json_val.items():
            if not _equal(value, back_json_val[key], strict):
                print("Dict at %s:" % key, value, back_json_val[key])
                ret = False
                break
    elif isinstance(json_val, list):
        ret = True
        for i, value in enumerate(json_val):
            if not _equal(value, back_json_val[i], strict):
                print("List at %s:" % i, value, back_json_val[i])
                ret = False
                break
    else:
        ret = (json_val == back_json_val)
        if not ret:
            print("Values not equal:", json_val, back_json_val)
    sys.stdout.flush()
    return ret


EASY_JSON = {'a': 1, 'b': 2, 'number': '12',
             'c': ['foo', {'bar': None, 'done': False}],
             'this_is_json': True}
HARD_JSON = {'a': 1, 'B': 2, 'number1': '12',
             'c': ['f oo -_?+@(*^&@#^$', {'Bar': None, 'DONE': False}],
             'This_isJson': True}


def test_simple_parse():
    converter = CLJsonConverter()
    res = converter.cl_from_json(EASY_JSON)
    print('CL JSON Result:', res.to_string())
    assert isinstance(res, KQMLList)
    assert len(res) == 2*len(EASY_JSON.keys())
    back_dict = converter.cl_to_json(res)
    assert len(back_dict) == len(EASY_JSON)
    assert _equal(EASY_JSON, back_dict)


def test_more_complex_parse():
    converter = CLJsonConverter()
    res = converter.cl_from_json(HARD_JSON)
    print("CL JSON Result:", res.to_string())
    assert isinstance(res, KQMLList)
    assert len(res) == 2*len(HARD_JSON.keys())
    back_dict = converter.cl_to_json(res)
    assert len(back_dict) == len(HARD_JSON)
    assert _equal(HARD_JSON, back_dict)


def test_simple_parse_w_token_bools():
    converter = CLJsonConverter(True)
    res = converter.cl_from_json(EASY_JSON)
    print('CL JSON Result:', res.to_string())
    assert isinstance(res, KQMLList)
    assert len(res) == 2*len(EASY_JSON.keys())
    back_dict = converter.cl_to_json(res)
    assert len(back_dict) == len(EASY_JSON)
    assert _equal(EASY_JSON, back_dict, strict=True)


def test_more_complex_parse_w_token_bools():
    converter = CLJsonConverter(True)
    res = converter.cl_from_json(HARD_JSON)
    print("CL JSON Result:", res.to_string())
    assert isinstance(res, KQMLList)
    assert len(res) == 2*len(HARD_JSON.keys())
    back_dict = converter.cl_to_json(res)
    assert len(back_dict) == len(HARD_JSON)
    assert _equal(HARD_JSON, back_dict, strict=True)


def _check_convert(inp, exp):
    cl_key = cl_json._key_from_string(inp)
    assert cl_key == exp, (cl_key, exp)
    original = cl_json._string_from_key(cl_key)
    assert original == inp, (original, inp)


def test_camelcase():
    _check_convert('helloKey', 'HELLO-KEY')


def test_single_capital_letter():
    _check_convert('B', '+B+')


def test_camel_starts_with_uppercase():
    _check_convert('HiStartsWithUpperCase', '*HI-STARTS-WITH-UPPER-CASE')


def test_join_by_underscore():
    _check_convert('joined_by_underscore', 'JOINED--BY--UNDERSCORE')


def test_json_all_caps():
    _check_convert('JSONAllCapitals', '+JSON+-ALL-CAPITALS')


def test_json_two_all_caps_words():
    _check_convert('TWO_WORDS', '+TWO-WORDS+')


def test_hell():
    _check_convert('camelCase_Mixed_4_PARTS', 'CAMEL-CASE--*MIXED--+4-PARTS+')
