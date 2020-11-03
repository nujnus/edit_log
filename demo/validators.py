# 自定义validator
from rest_framework.exceptions import ValidationError

# Function based
def even_number(value):
    if value % 2 != 0:
        raise ValidationError('This field must be an even number.')

# Class-based
class MultipleOf:
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if value % self.base != 0:
            message = 'This field must be a multiple of %d.' % self.base
            raise ValidationError(message)

def start_date_validator(value):
    # raise serializers.ValidationError('test ValidatorError.')
    return value


def end_date_validator(value):
    # raise serializers.ValidationError('test ValidatorError.')
    return value
    # if value  0:
    #    raise serializers.ValidationError('This field must be an even number.')
