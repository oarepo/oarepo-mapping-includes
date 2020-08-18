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
                                    'type': 'string'
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
