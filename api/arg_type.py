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


def integer(minimum=None, maximum=None):
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
