import unittest
import core.serial.disk.deserializers as des
from api.manager import Manager
from api.task import Task
from api.arg_type import string


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

