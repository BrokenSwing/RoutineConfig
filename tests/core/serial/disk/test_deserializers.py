import unittest
import core.serial.disk.deserializers as des
from api.manager import Manager
from api.task import Task
from api.arg_type import string
from api.routine import Routine


class TestDiskDeserializers(unittest.TestCase):

    def setUp(self) -> None:
        self.manager = Manager()
        self.t = Task("a task")
        self.t.register_argument("first arg", string(min_length=4))
        self.manager.register_task(self.t)

    def test_routine_deserialize(self):
        serialized_routine = {
            "name": "A simple routine",
            "tasks": [{
                "name": "a task",
                "values": {
                    "first arg": "my string"
                }
            }]
        }

        r = des.deserialize_routine(serialized_routine, self.manager)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "A simple routine")
        self.assertEqual(len(r.tasks), 1)
        t, values = r.tasks[0]
        self.assertEqual(self.t, t)
        self.assertDictEqual(values, {
            "first arg": "my string"
        })

    def test_routine_deserialize_invalid_value(self):
        serialized_routine = {
            "name": "A simple routine",
            "tasks": [{
                "name": "a task",
                "values": {
                    "first arg": "bad"
                }
            }]
        }

        r = des.deserialize_routine(serialized_routine, self.manager)
        self.assertIsNotNone(r)
        self.assertEqual(len(r.tasks), 0)

    def test_routine_deserialize_missing_task(self):
        serialized_routine = {
            "name": "A simple routine",
            "tasks": [{
                "name": "a non existing task",
                "values": {
                    "first arg": "my string"
                }
            }]
        }

        r = des.deserialize_routine(serialized_routine, self.manager)
        self.assertIsNotNone(r)
        self.assertEqual(len(r.tasks), 0)

    def test_routine_deserialize_missing_arg_value(self):
        serialized_routine = {
            "name": "A simple routine",
            "tasks": [{
                "name": "a task",
                "values": {}
            }]
        }

        r = des.deserialize_routine(serialized_routine, self.manager)
        self.assertIsNotNone(r)
        self.assertEqual(len(r.tasks), 0)

    def test_routine_deserialize_wrong_format_task(self):
        serialized_routine = {
            "name": "A simple routine",
            "tasks": [{
                "missing name": "a non existing task",
                "values": {
                    "first arg": "my string"
                }
            }]
        }

        r = des.deserialize_routine(serialized_routine, self.manager)
        self.assertIsNotNone(r)
        self.assertEqual(len(r.tasks), 0)

        serialized_routine = {
            "name": "A simple routine",
            "tasks": [{
                "name": ["Not", "a", "string"],
                "values": {
                    "first arg": "my string"
                }
            }]
        }

        r = des.deserialize_routine(serialized_routine, self.manager)
        self.assertIsNotNone(r)
        self.assertEqual(len(r.tasks), 0)

        serialized_routine = {
            "name": "A simple routine",
            "tasks": [{
                "name": "a task",
                "values": "not a dict"
            }]
        }

        r = des.deserialize_routine(serialized_routine, self.manager)
        self.assertIsNotNone(r)
        self.assertEqual(len(r.tasks), 0)

    def test_routine_deserialize_wrong_format(self):

        r = des.deserialize_routine({}, self.manager)
        self.assertIsNone(r)

        r = des.deserialize_routine({
            "name": 5,
            "tasks": []
        }, self.manager)
        self.assertIsNone(r)

        r = des.deserialize_routine({
            "name": "ok",
            "tasks": None
        }, self.manager)
        self.assertIsNone(r)

        # noinspection PyTypeChecker
        r = des.deserialize_routine("An other type", self.manager)
        self.assertIsNone(r)

    def test_card_deserialize_unlinked(self):
        card = des.deserialize_card({
            "name": "my card",
            "id": "the id"
        }, self.manager)
        self.assertEqual(card.name, "my card")
        self.assertEqual(card.id, "the id")
        self.assertFalse(card.is_linked())

    def test_card_deserialize_linked_not_found(self):
        card = des.deserialize_card({
            "name": "a card",
            "id": "an id"
        }, self.manager)
        self.assertEqual(card.name, "a card")
        self.assertEqual(card.id, "an id")
        self.assertFalse(card.is_linked())

    def test_card_deserialize_linked_found(self):
        routine = Routine("routine name")
        self.manager.add_routine(routine)
        card = des.deserialize_card({
            "name": "card name",
            "id": "card id",
            "target": "routine name"
        }, self.manager)
        self.assertTrue(card.is_linked())
        self.assertEqual(card.routine_name, "routine name")

    def test_card_deserialize_wrong_format(self):
        # noinspection PyTypeChecker
        self.assertIsNone(des.deserialize_card([], self.manager))
        self.assertIsNone(des.deserialize_card({}, self.manager))
        self.assertIsNone(des.deserialize_card({
            "name": 5,
            "id": "6546123"
        }, self.manager))
        self.assertIsNone(des.deserialize_card({
            "name": "a string",
            "id": {
                "other": "thing"
            }
        }, self.manager))
