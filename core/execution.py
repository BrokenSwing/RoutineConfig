from api.routine import Routine
import threading


class ExecutionThread(threading.Thread):

    def __init__(self, routine: Routine):
        threading.Thread.__init__(self, target=routine.execute_routine, daemon=True)
