import json


def test_included_pt(app):
    search = app.extensions['invenio-search']
    assert 'test-test-v1.0.0' in search.mappings
    with open(search.mappings['test-test-v1.0.0']) as f:
        data = json.load(f)
    assert data == {
        "mappings": {
            "date_detection": False,
            "numeric_detection": False,
            "dynamic": False,
            "properties": {
                "$schema": {
                    "type": "keyword",
                    "index": True
                },
                "test": {
                    "type": "string"
                },
                "nested": {
                    "type": "object",
                    "properties": {
                        "test": {
                            'properties': {
                                'dynamic-test': {
                                    'type': 'string',
                                    'extra': {
                                        'content': {},
                                        'content_pointer': '/mappings/properties/nested/properties/test',
                                        'id': 'dynamic-test',
                                        'json_pointer': None,
                                        'resource': 'dynamic',
                                        'type': 'dynamic#dynamic-test',
                                        'root': {
                                            'mappings': {
                                                'date_detection': False,
                                                'dynamic': False,
                                                'numeric_detection': False,
                                                'properties': {
                                                    '$schema': {
                                                        'index': True,
                                                        'type': 'keyword'
                                                    },
                                                    'nested': {
                                                        'properties': {'test': {}},
                                                        'type': 'object'
                                                    },
                                                    'nested2': {
                                                        'properties': {'test': {
                                                            'type': 'included-v1.0.0.json#/test'}},
                                                        'type': 'object'
                                                    },
                                                    'test': {'type': 'string'}
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            'type': 'object'
                        }
                    }
                },
                "nested2": {
                    "type": "object",
                    "properties": {
                        "test": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
