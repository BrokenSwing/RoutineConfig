from api.routine import Routine


def serialize_routine(routine: Routine) -> dict:
    """
    Serializes a routine to be saved on the disk

    :param routine: the routine to serialize
    :return: the serialized version of the routine as a dict, to be saved on disk
    """
    return {
        "name": routine.name,
        "tasks": [{"name": task.name, "values": values} for task, values in routine.tasks],
    }
