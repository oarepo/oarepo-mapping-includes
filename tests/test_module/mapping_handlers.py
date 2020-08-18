def dynamic(resource, json_pointer):
    return {
        "type": "object",
        "properties": {
            json_pointer: {
                "type": "string"
            }
        }
    }
