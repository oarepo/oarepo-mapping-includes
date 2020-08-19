import pytest

from oarepo_mapping_includes.ext import IncludedMapping


def test_json_pointer():
    m = IncludedMapping('test', {
        'a': {
            'b': 1
        }
    })

    assert m.get_pointer(None) == m.json
    assert m.get_pointer('') == m.json

    assert m.get_pointer('/a') == {
        'b': 1
    }

    assert m.get_pointer('/a/b') == 1

    with pytest.raises(KeyError, match='Json pointer /c not found in test: member \'c\' not found'):
        assert m.get_pointer('/c')


def test_ids():
    m = IncludedMapping('test', {
        'a': {
            '$id': 'aa',
            'b': {
                "$id": 'bb',
                'test': '1'
            }
        }
    })

    assert m.get_id('') == m.json
    assert m.get_id(None) == m.json

    assert m.get_id('aa') == {
        'b': {
            'test': '1'
        }
    }

    assert m.get_id('bb') == {
        'test': '1'
    }

    with pytest.raises(KeyError, match='Id cc not found in test'):
        assert m.get_id('cc')
