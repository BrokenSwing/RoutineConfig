import unittest
import core.serial.rest.serializers as serial
from api.task import Task
from api.routine import Routine
import api.arg_type as arg_type


class TestRESTSerializers(unittest.TestCase):

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

    def test_task_serialization(self):
        task = Task("My task")
        task.register_argument("the arg", arg_type.choice("One", "Two"))

        serialized = serial.serialize_task(task)
        self.assertDictEqual(serialized, {
            "name": "My task",
            "arguments": {
                "the arg": {
                    "type": "choice",
                    "choices": ["One", "Two"]
                }
            }
        })


if __name__ == '__main__':
    unittest.main()
