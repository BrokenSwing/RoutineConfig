import unittest
from api.manager import Manager
from api.routine import Routine
from api.task import Task
from api.card import Card


class TestManager(unittest.TestCase):

    def setUp(self):
        self.manager = Manager()
        self.task = Task("the task")
        self.routine = Routine("the routine")
        self.card = Card("the card id", "the card name")

    def test_manager_default_state(self):
        self.assertEqual(len(self.manager.tasks), 0)
        self.assertEqual(len(self.manager.routines), 0)
        self.assertEqual(len(self.manager.cards), 0)

    """
        Tasks tests
    """

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
        self.assertIsNone(self.manager.find_task("unknown task"))

    """
        Routine tests
    """

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
        self.assertIsNone(self.manager.find_routine("unknown routine"))

    def test_remove_routine(self):
        self.manager.add_routine(self.routine)
        self.manager.remove_routine("the routine")
        self.assertEqual(len(self.manager.routines), 0)

    """
        Card tests
    """

    def test_add_card(self):
        self.manager.add_card(self.card)
        self.assertEqual(len(self.manager.cards), 1)

    def test_override_card(self):
        other_card = Card("the card id", "other name")
        self.manager.add_card(self.card)
        self.manager.add_card(other_card)
        self.assertEqual(len(self.manager.cards), 1)
        self.assertIs(other_card, self.manager.cards["the card id"])

    def test_find_card_by_id(self):
        self.manager.add_card(self.card)
        card = self.manager.find_card_by_id("the card id")
        self.assertIs(self.card, card)
        self.assertIsNone(self.manager.find_card_by_id("unknown id"))

    def test_find_card_by_name(self):
        self.manager.add_card(self.card)
        card = self.manager.find_card_by_name("the card name")
        self.assertIs(self.card, card)
        self.assertIsNone(self.manager.find_card_by_name("unknown name"))

