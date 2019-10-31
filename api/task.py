class Task:
    """
    Abstract class defining a task. A task is an atomic action (i.e: switch on/off light, play music, etc ...)
    It can take arguments which will be defined by the user (i.e: turn off light between 9 am and 1 pm. 9 and 1
    can be defined as parameters given by user).
    """

    def __init__(self, name: str):
        assert len(name) > 0, "A task name can't be empty"
        self.name = name
        self.arguments = {}

    def register_argument(self, name: str, arg_type: dict):
        """
        Registers an argument with the specified name and the specified type. This argument will then be filled up
        by user.
        Example:
            import arg_type
            register_argument("age", arg_type.integer(min=0))

        :param name: the argument name (str)
        :param arg_type: the argument type (dict: {type: str}), please use arg_type package to specify this argument
        """
        assert "type" in arg_type, "Argument 'arg_type' must contain key 'type'"

        if name in self.arguments:
            print("[WARNING] Task {} registers two arguments with the same name ({}). "
                  "Second registration will override first one.".format(self.name, name))

        self.arguments[name] = arg_type

    def on_validation(self, arg_values):
        """
        Called when user entered valid arguments. You can use this method to perform additional checks on values
        (i.e if an argument correspond to a website url, ping this website to see if it exists).

        :param arg_values: a dict mapping arguments name to their value
        :return: a tuple containing two values. The first one indicates if the values for arguments are still valid,
        the second one is the error message which will be displayed in case the first value is False
        """
        return True, None

    def execute_task(self, arg_values):
        """
        Executes the action corresponding to the task.

        :param arg_values: a dict linking each argument name to it's value
        """
        print("The task {} does nothing when ran.".format(self.name))
