import unittest
from api.card import Card
from api.routine import Routine


class TestCard(unittest.TestCase):

    def test_card_name_must_not_be_empty(self):
        with self.assertRaises(AssertionError):
            Card("the card id", "")

    def test_card_id_must_not_be_empty(self):
        with self.assertRaises(AssertionError):
            Card("", "the card name")

    def test_card_link(self):
        card = Card("card id", "card name")
        routine = Routine("routine name")
        self.assertFalse(card.is_linked())

        card.link_to(routine)
        self.assertTrue(card.is_linked())
        self.assertEqual(card.routine_name, "routine name")

        card.unlink()
        self.assertFalse(card.is_linked())
