from api.routine import Routine
from api.card import Card


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


def serialize_card(card: Card) -> dict:
    """
    Serializes a card to be saved on disk

    :param card: the card to serialize
    :return: the serialized version of the card as a dict, to be saved on disk
    """
    obj = {
        "id": card.id,
        "name": card.name,
    }
    if card.is_linked():
        obj["target"] = card.routine_name
    return obj
