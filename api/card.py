from api.routine import Routine


class Card:

    def __init__(self, card_id: str, name: str):
        assert len(card_id) > 0, "Card id must not be empty"
        assert len(name) > 0, "Card name must not be empty"
        self.id = card_id
        self.name = name
        self.routine_name = None

    def is_linked(self) -> bool:
        return self.routine_name is not None

    def link_to(self, routine: Routine):
        self.routine_name = routine.name

    def unlink(self):
        self.routine_name = None
