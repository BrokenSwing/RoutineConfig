import re


def validate(arg_type: dict, value: any) -> bool:
    """
    Validates any known argument type.

    :param arg_type: argument type from api.arg_type
    :param value: the value to validate for this argument
    :return: True if the value if valid for the given argument type, else False
    """
    if arg_type["type"] == "integer" and (type(value) == int or type(value) == str):
        if type(value) == str:
            try:
                value = int(value)
            except ValueError:
                return False
        return validate_integer_arg(arg_type, int(value))
    if arg_type["type"] == "choice" and type(value) == str:
        return validate_choice_arg(arg_type, value)
    if arg_type["type"] == "string" and type(value) == str:
        return validate_string_arg(arg_type, value)
    return False


def validate_integer_arg(arg: dict, value: int) -> bool:
    """
    Checks if the given value matches constraints of integer argument (from api.arg_type).
    If arg has min value, checks if value is equal to or greater than this min value.
    If arg has max value, checks if value is equal to or lower than this max value.

    :param arg: the integer argument
    :param value: the value to validate
    :return: True if the value passes checks, else False
    """
    if "min" in arg and value < arg["min"]:
        return False
    if "max" in arg and value > arg["max"]:
        return False
    return True


def validate_choice_arg(arg: dict, value: str) -> bool:
    """
    Checks if the given value matches constraints of choice argument (from api.arg_type).
    It checks if the given value is in the list of choices defined in argument type

    :param arg: the choice argument
    :param value: the value to validate
    :return: True if the value passes checks, else False
    """
    return value in arg["choices"]


def validate_string_arg(arg: dict, value: str) -> bool:
    """
    Checks if the given value matched constraints of string argument (from api.arg_type).
    If arg has a regex defined, it checks value matches this regex.
    If arg has a min_length, it checks value is longer than or equal to min_length
    If arg has a max_length, it checks value is shorter than or equal to max_length

    :param arg: the string argument
    :param value: the value to validate
    :return: True if the value passes checks, else False
    """
    if "regex" in arg and re.search(arg["regex"], value) is None:
        return False
    if "min_length" in arg and len(value) < arg["min_length"]:
        return False
    if "max_length" in arg and len(value) > arg["max_length"]:
        return False
    return True
