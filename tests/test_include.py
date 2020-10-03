import json


def test_included_pt(app):
    search = app.extensions['invenio-search']
    assert 'test-test-v1.0.0' in search.mappings
    with open(search.mappings['test-test-v1.0.0']) as f:
        data = json.load(f)
    assert data == {
        'mappings': {
            'date_detection': False,
            'dynamic': False,
            'numeric_detection': False,
            'properties': {
                '$schema': {
                    'index': True,
                    'type': 'keyword'
                },
                'a': {
                    'properties': {
                        'd': {
                            'type': 'string'
                        }
                    },
                    'type': 'object'
                },
                'b': {
                    'properties': {
                        'c': {
                            'type': 'string'
                        },
                        'test': {
                            'properties': {
                                'dynamic-test': {
                                    'extra': {
                                        'content': {},
                                        'content_pointer': '/mappings/properties/nested/properties/test',
                                        'id': 'dynamic-test',
                                        'json_pointer': None,
                                        'resource': 'dynamic',
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
                                                    'a': {'type': 'included2-v1.0.0.json#/a'},
                                                    'b': {'type': 'included2-v1.0.0.json#/b'},
                                                    'nested': {
                                                        'properties': {
                                                            'test': {}
                                                        },
                                                        'type': 'object'
                                                    },
                                                    'nested2': {
                                                        'properties': {
                                                            'test': {
                                                                'type': 'included-v1.0.0.json#/test'
                                                            }
                                                        },
                                                        'type': 'object'
                                                    },
                                                    'test': {
                                                        'type': 'string'
                                                    }
                                                }
                                            }
                                        },
                                        'type': 'dynamic#dynamic-test'
                                    },
                                    'type': 'string'
                                }
                            },
                            'type': 'object'
                        }
                    },
                    'type': 'object'
                },
                'nested': {
                    'properties': {
                        'test': {
                            'properties': {
                                'dynamic-test': {
                                    'extra': {
                                        'content': {},
                                        'content_pointer': '/mappings/properties/nested/properties/test',
                                        'id': 'dynamic-test',
                                        'json_pointer': None,
                                        'resource': 'dynamic',
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
                                                    'a': {'type': 'included2-v1.0.0.json#/a'},
                                                    'b': {'type': 'included2-v1.0.0.json#/b'},
                                                    'nested': {
                                                        'properties': {
                                                            'test': {}
                                                        },
                                                        'type': 'object'
                                                    },
                                                    'nested2': {
                                                        'properties': {
                                                            'test': {
                                                                'type': 'included-v1.0.0.json#/test'
                                                            }
                                                        },
                                                        'type': 'object'
                                                    },
                                                    'test': {
                                                        'type': 'string'
                                                    }
                                                }
                                            }
                                        },
                                        'type': 'dynamic#dynamic-test'
                                    },
                                    'type': 'string'
                                }
                            },
                            'type': 'object'
                        }
                    },
                    'type': 'object'
                },
                'nested2': {
                    'properties': {
                        'test': {
                            'type': 'string'
                        }
                    },
                    'type': 'object'
                },
                'test': {
                    'type': 'string'
                }
            }
        }
    }
