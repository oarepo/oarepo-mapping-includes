import pytest
import requests_mock


def test_load_internal_resource(app):
    includes = app.extensions['oarepo-mapping-includes']

    assert includes.load_type('dynamic#blah', content={}, root={}, content_pointer='') == {
        "type": "object",
        "properties": {
            'blah': {
                "type": "string",
                'extra': {
                    'content': {},
                    'content_pointer': '',
                    'root': {},
                    'id': 'blah',
                    'json_pointer': None,
                    'resource': 'dynamic',
                    'type': 'dynamic#blah'
                },
            }
        }
    }


def test_dynamic_on_type(app):
    includes = app.extensions['oarepo-mapping-includes']

    assert includes.load_type('dynamic2', content={}, root={}, content_pointer='') == {
        'dynamic2': True
    }


def test_not_existing(app):
    includes = app.extensions['oarepo-mapping-includes']

    with pytest.raises(KeyError, match='not-existing not in \\[\'included-v1.0.0.json\'\\]'):
        includes.load_type('not-existing#blah', content={}, root={}, content_pointer='')


def test_http(app):
    includes = app.extensions['oarepo-mapping-includes']

    with requests_mock.Mocker() as m:
        m.get('http://test.com/included#blah', text='{"$id": "blah", "included": true}')
        assert includes.load_type('http://test.com/included',
                                  content={}, root={}, content_pointer='') == {
            'included': True
        }
