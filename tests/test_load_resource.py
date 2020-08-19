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
