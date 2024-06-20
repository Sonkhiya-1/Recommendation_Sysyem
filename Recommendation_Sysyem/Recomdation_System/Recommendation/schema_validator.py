import jsonschema
import json

schemas = {
    'view_menu': {
        'type': 'object',
        'properties': {
            'action': {'type': 'string'}
        },
        'required': ['action']
    },
    # Define schemas for other actions
}

def validate_request(action, data):
    schema = schemas.get(action)
    if not schema:
        raise ValueError(f"No schema defined for action {action}")
    jsonschema.validate(instance=data, schema=schema)
