from jsonschema.validators import extend
from jsonschema.validators import Draft4Validator
from jsonschema.exceptions import ValidationError
from jsonschema._utils import format_as_index
import json
import re

SCHEMA_PATH = ""


def get_property(message):
    result = re.search("u''", message)
    return result.group(1)


def get_json(path):
    with open(path) as f:
        return json.load(f)


def recommended_draft4(validator, required, instance, schema):
    if not validator.is_type(instance, "object"):
        return
    for prop in required:
        if prop not in instance:
            yield ValidationError("%r is a recommended property" % prop)

Draft4ValidatorExtended = extend(
    validator=Draft4Validator,
    validators={u"recommended": recommended_draft4},
    version="draft4e"
)


def is_integer(text):
    try:
        int(text)
        return True
    except ValueError:
        return False


def validate_item(item):
    file_name = item['type'].rsplit('/', 1)[1]
    schema = get_json(file_name + '.json')
    instance = item['properties']
    Draft4ValidatorExtended.check_schema(schema)
    validator = Draft4ValidatorExtended(schema)
    validation = {'required_missing': [], 'recommended_missing': [],
                  'bad_cardinality': [], 'bad_type': [], 'full_report': ''}
    for error in validator.iter_errors(instance):
        field = error.message.split("'")[1]
        if 'required' in error.message:
            validation['required_missing'].append(field)
        elif 'recommended' in error.message:
            validation['recommended_missing'].append(field)
        elif error.validator == 'oneOf':
            valid_types = []
            for valid_schema in error.schema['oneOf']:
                if valid_schema['type'] != 'object':
                    valid_types.append(valid_schema['type'])
                else:
                    if 'enum' in valid_schema['properties']['type']:
                        for valid_type in valid_schema['properties']['type']['enum']:
                            valid_types.append(valid_type)
            if isinstance(error.instance, list) and 'array' not in valid_types:
                validation['full_report'] += 'Cardinality fail, you must provide only one value for: '\
                                             + str(error.relative_path) + '\n'
                validation['bad_cardinality'].append(error.relative_path[0])
            elif is_integer(error.instance) and 'integer' in valid_types:
                continue
            else:
                if 'array' in valid_types:
                    valid_types.remove('array')
                validation['bad_type'].append(error.relative_path[0])
                validation['full_report'] += 'One of the ' + str(error.relative_path) +\
                                             ' values is not any of the valid types: ' + str(valid_types) + '\n'
                validation['full_report'] += ' Value: ' + str(error.instance)
    return validation

