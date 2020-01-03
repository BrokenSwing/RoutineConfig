import unittest
import core.serial.disk.serializers as serial
from api.task import Task
from api.routine import Routine
from api.card import Card
import api.arg_type as arg_type


class TestDiskSerializers(unittest.TestCase):

    def test_routine_serialization(self):
        routine = Routine("My routine")

        task1 = Task("Task 1")
        task1.register_argument("arg1", arg_type.integer(minimum=0))

        task2 = Task("Task 2")
        task2.register_argument("arg1", arg_type.choice("Yes", "No"))
        task2.register_argument("arg2", arg_type.integer(maximum=909))

        routine.add_task(task1, {"arg1": 10})
        routine.add_task(task2, {"arg1": "Yes", "arg2": 700})

        serialized = serial.serialize_routine(routine)
        self.assertDictEqual(serialized, {
            "name": "My routine",
            "tasks": [{
                "name": "Task 1",
                "values": {
                    "arg1": 10
                },
            }, {
                "name": "Task 2",
                "values": {
                    "arg1": "Yes",
                    "arg2": 700
                }
            }]
        })

    def test_card_serialization(self):
        card = Card("card id", "card name")
        self.assertDictEqual(serial.serialize_card(card), {
            "name": "card name",
            "id": "card id",
        })

        routine = Routine("routine name")
        card = Card("the card id", "the card name")
        card.link_to(routine)
        self.assertDictEqual(serial.serialize_card(card), {
            "name": "the card name",
            "id": "the card id",
            "target": "routine name"
        })
