import unittest
from api.manager import Manager
from api.routine import Routine
from api.task import Task


class TestManager(unittest.TestCase):

    def setUp(self):
        self.manager = Manager()
        self.task = Task("the task")
        self.routine = Routine("the routine")

    def test_register_task(self):
        self.manager.register_task(self.task)
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertIs(self.task, self.manager.tasks["the task"])

    def test_override_task(self):
        other_task = Task("the task")
        self.manager.register_task(self.task)
        self.manager.register_task(other_task)
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertIs(other_task, self.manager.tasks["the task"])

    def test_find_task(self):
        self.manager.register_task(self.task)
        task = self.manager.find_task("the task")
        self.assertIs(self.task, task)

    def test_add_routine(self):
        self.manager.add_routine(self.routine)
        self.assertEqual(len(self.manager.routines), 1)

    def test_override_routine(self):
        other_routine = Routine("the routine")
        self.manager.add_routine(self.routine)
        self.manager.add_routine(other_routine)
        self.assertEqual(len(self.manager.routines), 1)
        self.assertIs(other_routine, self.manager.routines["the routine"])

    def test_find_routine(self):
        self.manager.add_routine(self.routine)
        routine = self.manager.find_routine("the routine")
        self.assertIs(self.routine, routine)

    def test_remove_routine(self):
        self.manager.add_routine(self.routine)
        self.manager.remove_routine("the routine")
        self.assertEqual(len(self.manager.routines), 0)


if __name__ == '__main__':
    unittest.main()
