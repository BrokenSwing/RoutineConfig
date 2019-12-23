import re


def choice(*args):
    """
    Creates a choice argument type. The user will be able to choose one of given possibilities.
    Example:
        choice("quickly", "slowly")

    :param args: a list of string the user will be able to choose
    :return: a dict representing this argument type with the appropriate format to be used by the JS front-end script
    """
    assert len(args) > 0, "You must specify at least one choice"
    return {
        "type": "choice",
        "choices": [c for c in args]
    }


def integer(minimum: int = None, maximum: int = None):
    """
    Creates an integer argument type.

    :param minimum: the minimum value the argument can take (optional)
    :param maximum: the maximum value the argument can take (optional)
    :return: a dict representing this argument type with the appropriate format to be used by the JS front-end script
    """
    desc = {
        "type": "integer",
    }
    if minimum is not None and maximum is not None:
        assert int(minimum) <= int(maximum), \
            "Expected minimum to be lower or equal to maximum. Got min: {} and max: {}".format(minimum, maximum)
    if minimum is not None:
        desc["min"] = int(minimum)
    if maximum is not None:
        desc["max"] = int(maximum)
    return desc


def string(regex: str = None, min_length: int = None, max_length: int = None):
    """
    Creates a string argument type.
    The provided string in regex must be a valid regular expression, unpredictable behavior is expected if it's not the
    case.
    If both min_length and max_length are specified, min_length must be lower than or equal to max_length.

    :param regex: a regular expression that will be used to validate argument format
    :param min_length: the minimum length for the string
    :param max_length: the maximum length for the string
    :return: a dict representing this argument type with the appropriate format to be sued by the JS front-end script
    """
    desc = {
        "type": "string",
    }
    if regex is not None:
        desc["regex"] = regex
    if min_length is not None and max_length is not None:
        assert int(min_length) <= int(max_length), \
            "Expected min_length to be lower than or equal to max_length. " \
            "Got min_length: {} and max_length: {}".format(min_length, max_length)
    if min_length is not None:
        desc["min_length"] = int(min_length)
    if max_length is not None:
        desc["max_length"] = int(max_length)
    return desc
