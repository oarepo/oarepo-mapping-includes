from copy import deepcopy


def dynamic(type=None, resource=None, id=None, json_pointer=None,
            app=None, content=None, root=None, content_pointer=None):
    assert type is not None
    assert app is not None
    assert content is not None
    assert root is not None
    assert content_pointer is not None

    return {
        "type": "object",
        "properties": {
            id: {
                "type": "string",
                "extra": {
                    "content": deepcopy(content),
                    "root": deepcopy(root),
                    "content_pointer": content_pointer,
                    'type': type,
                    'resource': resource,
                    'id': id,
                    'json_pointer': json_pointer,
                }
            }
        }
    }
