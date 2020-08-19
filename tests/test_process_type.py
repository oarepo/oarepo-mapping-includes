from oarepo_mapping_includes.ext import IncludedMapping, OARepoMappingIncludesState
from oarepo_mapping_includes.mapping_transformer import process_type


def test_no_type():
    assert process_type(
        {'type': 'string'}, 'type',
        OARepoMappingIncludesState(
            None,
            {
                'string': IncludedMapping('string', {'test': True})
            }, {})
    ) == {
               'type': 'string',
               'test': True
           }


def test_infinite_recursion():
    assert process_type(
        {'type': 'string'}, 'type',
        OARepoMappingIncludesState(
            None,
            {
                'string': IncludedMapping('string', {'test': True, 'type': 'string'})  # infinite recursion on type
            }, {})
    ) == {
               'type': 'string',
               'test': True
           }


def test_break_recursion():
    assert process_type(
        {'type': 'string'}, 'type',
        OARepoMappingIncludesState(
            None,
            {
                # break recursion on string2 and do not continue with the next rule
                'string': IncludedMapping('string', {'test': True, 'oarepo:type': 'string2'}),
                'string2': IncludedMapping('string', {'test': False})
            }, {})
    ) == {
               'type': 'string2',
               'test': True
           }


def test_mapping_not_found():
    assert process_type(
        {'type': 'string'}, 'type',
        OARepoMappingIncludesState(
            None,
            {}, {})
    ) == {
               'type': 'string'
           }
