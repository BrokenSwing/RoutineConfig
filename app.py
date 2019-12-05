from flask import Flask, render_template, request
from api.manager import Manager
from api.task import Task
import api.arg_type as arg_type
from api.routine import Routine

app = Flask(__name__)
manager = Manager()
task = Task("My task")
task.register_argument("Action", arg_type.choice("Allumer", "Eteindre"))
task.register_argument("Value", arg_type.integer(minimum=0, maximum=50))
task.execute_task = lambda x: print("Task ran")
manager.register_task(task)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/routines", methods=["GET", "POST"])
def routines():
    error = None
    success = None

    if request.method == "POST":
        try:
            action = request.form["action"]
        except KeyError:
            action = ""

        try:
            value = request.form["value"]
        except KeyError:
            value = ""

        if action == "run":
            r = manager.find_routine(value)
            if r is not None:
                r.execute_routine()
                success = "La routine s'est lancé sans erreur"
            else:
                error = "Impossible de trouver une routine avec ce nom."
        elif action == "delete":
            r = manager.find_routine(value)
            if r is not None:
                manager.remove_routine(r.name)
                success = "La routine a bien été supprimée"
            else:
                error = "Impossible de trouver une routine avec ce nom."
        elif action == "create":
            if len(value) == 0:
                error = "La nom de la routine ne doit pas être vide."
            elif len(value) > 40:
                error = "Le nom de la routine ne peut dépasser 40 charctères."
            elif manager.find_routine(value) is None:
                r = Routine(value)
                manager.add_routine(r)
                success = "La routine a bien été créée."
            else:
                error = "Une routine avec ce nom existe déjà."

    return render_template("routines.html", routines=manager.routines.values(), error=error, success=success)


if __name__ == '__main__':
    app.run()
