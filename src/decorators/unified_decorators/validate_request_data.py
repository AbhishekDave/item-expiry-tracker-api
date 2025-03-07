# src/decorators/unified_decorators/validate_request_data

from functools import wraps
from flask import request, jsonify, g
from marshmallow import ValidationError

from src.utils.error_handling_utility.exceptions import MethodNotAllowedException, UnsupportedMediaTypeException, MissingDataException


def validate_request_data(method, schema_dict=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if the request method matches the specified method
            if request.method != method:
                raise MethodNotAllowedException('Method not allowed.')

            # Check Content-Type
            if request.content_type != 'application/json':
                raise UnsupportedMediaTypeException('Content-Type must be application/json.')

            # Check if JSON data is provided
            data = request.get_json()
            if not data:
                raise MissingDataException('No input data provided.')

            # Validate data using multiple Marshmallow schemas
            if schema_dict:
                validated_data = {}
                try:
                    for key, schema_class in schema_dict.items():
                        if key in data:
                            schema = schema_class()
                            validated_data[key] = schema.load(data[key])
                        else:
                            raise ValidationError({key: ['Missing data for required field.']})

                    # Store validated data in g for global access
                    g.validated_data = validated_data
                except ValidationError as err:
                    return jsonify(err.messages), 400

            return f(*args, **kwargs)

        return decorated_function

    return decorator
