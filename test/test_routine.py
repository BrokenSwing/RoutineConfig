import unittest
from api.routine import Routine
import api.task


class TestRoutine(unittest.TestCase):

    def setUp(self):
        self.task = api.task.Task("task for routine test")

    def test_empty_name(self):
        with self.assertRaises(AssertionError):
            Routine("")

    def test_add_task(self):
        routine = Routine("my routine")
        routine.add_task(self.task, {"arg1": 1})
        self.assertEqual(len(routine.tasks), 1)

        task, values = routine.tasks[0]
        self.assertIs(self.task, task)
        self.assertDictEqual(values, {"arg1": 1})

    def test_remove_task(self):
        routine = Routine("my routine")
        routine.add_task(self.task, {"a": "b"})
        task, values = routine.remove_task(0)

        self.assertIs(self.task, task)
        self.assertDictEqual(values, {"a": "b"})
        self.assertEqual(len(routine.tasks), 0)

    def test_modify_task(self):
        routine = Routine("my routine")
        routine.add_task(self.task, {"old": "values"})
        routine.modify_task(0, {"new": "super value"})
        task, values = routine.tasks[0]

        self.assertIs(self.task, task)
        self.assertDictEqual(values, {"new": "super value"})

    def test_execute_routine_calls_tasks(self):
        routine = Routine("the routine")

        def raise_exception(argument):
            raise Exception()

        self.task.execute_task = raise_exception
        routine.add_task(self.task, {})
        with self.assertRaises(Exception):
            routine.execute_routine()

    def test_execute_routine_passes_args(self):
        routine = Routine("other routine")

        def check_args(arguments):
            self.assertDictEqual(arguments, {
                "one": 1,
                "two": 2
            })

        self.task.execute_task = check_args
        routine.add_task(self.task, {
            "one": 1,
            "two": 2
        })
        routine.execute_routine()


if __name__ == '__main__':
    unittest.main()
