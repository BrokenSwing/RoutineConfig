from api.task import Task
from api.routine import Routine
from api.card import Card


class Manager:
    """
    This class is used to manage all known tasks and routines. It's kind of a collection of tasks and routines.
    """

    def __init__(self):
        self.tasks = {}
        self.routines = {}
        self.cards = {}

    def register_task(self, task: Task):
        """
        Registers a task user will be able to add to a routine using web interface.
        If you register two tasks with having the same name, the second one will override the first one.

        :param task: the task to register
        """
        if task.name in self.tasks:
            print("[WARNING] Task with name {} will override task registered with the same name".format(task.name))
        self.tasks[task.name] = task

    def add_routine(self, routine: Routine):
        """
        Registers a routine, the user will be able to see, modify and delete this routine using web interface.
        If you register two routines with having the same name, the second one will override the first one.

        :param routine: the routine to register
        """
        if routine.name in self.routines:
            print("[WARNING] Routine with name {} will override routine registered with the same name"
                  .format(routine.name))
        self.routines[routine.name] = routine

    def remove_routine(self, routine_name) -> Routine or None:
        """
        Removes the routine with the given name if it exists.

        :param routine_name: the name of the routine to remove
        :return: the removed routine or None if no routine with the given name was find
        """
        if routine_name in self.routines:
            routine = self.routines[routine_name]
            del self.routines[routine_name]
            return routine
        return None

    def find_task(self, task_name: str) -> Task or None:
        """
        Finds the task with the given name.

        :param task_name: the name of the task to find
        :return: the task with the given name or None if no task with the given name was find
        """
        return self.tasks[task_name] if task_name in self.tasks else None

    def find_routine(self, routine_name: str) -> Routine or None:
        """
        Finds the routine with the given name.

        :param routine_name: the name of the routine to find
        :return: the routine with the given name or None if no routine with the given name was find
        """
        return self.routines[routine_name] if routine_name in self.routines else None

    def add_card(self, card: Card):
        """
        Adds a card to the manager

        :param card: the card to add
        """
        if card.id in self.cards:
            print("[WARNING] Card with id {} already exists. It will override it.".format(card.id))
        self.cards[card.id] = card

    def find_card_by_id(self, card_id) -> Card or None:
        """
        Retrieves a card from its id.

        :param card_id: the id of the card to retrieve
        :return: the card with the given id, or None if a such card can't be found
        """
        if card_id in self.cards:
            return self.cards[card_id]
        return None

    def find_card_by_name(self, card_name) -> Card or None:
        """
        Retrieves a card from its name.

        :param card_name: the name of the card to retrieve
        :return: the first card with the given name, or None if no card with a such name exists
        """
        for card_id in self.cards:
            if self.cards[card_id].name == card_name:
                return self.cards[card_id]
        return None

    def remove_card(self, card_id) -> Card or None:
        """
        Removes the card with the given id from the manager.

        :param card_id: the id of the card to remove
        :return: the removed card if a card with such an id exists, else None
        """
        if card_id in self.cards:
            card = self.cards[card_id]
            del self.cards[card_id]
            return card
        return None
