from api.task import Task


class Routine:
    """
    This class represents a collection of tasks with the parameterized values for their corresponding arguments.
    When executed, this routine will run all tasks associated with it.
    """

    def __init__(self, name: str):
        """
        Creates a new routine with the given name. The name must be unique between all existing routines.

        :param name: the name for the routine, must not be empty
        """
        assert len(name) > 0, "The routine name must not be empty"
        self.name = name
        self.tasks = []

    def add_task(self, task: Task, arguments: dict):
        """
        Adds a task to the routine.

        :param task: the task to add
        :param arguments: the values for the task's arguments
        """
        self.tasks.append((task, arguments))

    def remove_task(self, index: int):
        """
        Removes the task at the given index. If you don't know the index for the task you want to remove, you have
        to loop on tasks field and scan for the targeted task.
        The index for a task isn't constant over time, each time a task is removed, all tasks after the one removed
        will see their index to be shifted down by one.

        :param index: the index for the task to remove
        :return: the removed task

        :raises IndexError: if the given index is greater than or equal to the task count
        """
        return self.tasks.pop(index)

    def modify_task(self, index: int, arguments: dict):
        """
        Sets a new arguments values for the task at the given index. If you have trouble finding the index, please
        read documentation for Routine::remove_task.
        This method does not perform any kind of verification on arguments values.

        :param index: the index for the task to modify
        :param arguments: the new values for the arguments
        :raises IndexError: if the given index is greater than or equal to the task count
        """
        task, old_values = self.tasks[index]
        self.tasks[index] = (task, arguments)

    def execute_routine(self):
        """
        Executes all the tasks attached to this routine with the arguments values provided before using
        Routine::add_task and Routine::modify_task.
        """
        for task, args in self.tasks:
            task.execute_task(args)
