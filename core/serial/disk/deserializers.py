from api.routine import Routine
from api.manager import Manager
from core.validation import validate


def deserialize_routine(obj: dict, manager: Manager) -> Routine or None:
    """
    Deserialize a routine from the given dict using the tasks registered in the given manager.
    If some referenced tasks are missing, they're discarded from the routine.
    This function doesn't add deserialized routine to given manager.

    :param obj: the serialized routine (serialized using core.serial.disk.serializers.serialize_routine)
    :param manager: the manager where we should lookup to find tasks referenced by the routine
    :return: the deserialized routine or None if the given obj doesn't match expected format
    """
    if type(obj) is not dict:
        return None
    if "name" not in obj or "tasks" not in obj:
        return None
    if type(obj["name"]) is not str or type(obj["tasks"]) is not list:
        return None

    name = obj["name"]
    tasks = obj["tasks"]

    routine = Routine(name)

    for task in tasks:
        if type(task) is not dict:
            continue
        if "name" not in task or "values" not in task:
            continue
        if type(task["name"]) is not str or type(task["values"]) is not dict:
            continue

        t = manager.find_task(task["name"])
        if t is None:
            continue

        values = task["values"]
        valid = True
        for arg_name in t.arguments:
            if arg_name not in values:
                valid = False
                break
            if not validate(t.arguments[arg_name], values[arg_name]):
                valid = False
                break

        if not valid:
            continue

        if t.on_validation(values):
            routine.add_task(t, values)

    return routine
