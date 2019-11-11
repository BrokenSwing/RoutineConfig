from api.task import Task
from api.routine import Routine


def serialize_task(task: Task) -> dict:
    """
    Serializes a task to be sent to client through REST API.

    :param task: the task to serialize
    :return: the serialized version of the task as a dict, to be sent through REST API
    """
    return {
        "name": task.name,
        "arguments": task.arguments
    }


def serialize_routine(routine: Routine) -> dict:
    """
    Serializes a routine to be sent to client through REST API.

    :param routine: the routine to serialize
    :return: the serialized version of the task as a dict, to be sent through REST API
    """
    return {
        "name": routine.name,
        "tasks": [{"name": task.name, "values": values} for task, values in routine.tasks],
    }
