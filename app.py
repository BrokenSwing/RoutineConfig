from flask import Flask, render_template, request, abort, redirect
from api.manager import Manager
from api.task import Task
import api.arg_type as arg_type
from api.routine import Routine
from api.card import Card
from core import validation
from core import execution
from core.serial.disk import serializers as serial
from core.serial.disk import deserializers as des
import json


app = Flask(__name__)
manager = Manager()
task = Task("My task")
task.register_argument("Action", arg_type.choice("Allumer", "Eteindre"))
task.register_argument("Value", arg_type.integer(minimum=0, maximum=50))
task.register_argument("Phrase", arg_type.string(regex="^c", min_length=1, max_length=10))
manager.register_task(task)


def save_manager():
    serialized_routines = [serial.serialize_routine(r) for r in manager.routines.values()]
    with open("manager_store.json", "w") as file:
        file.write(json.dumps({"routines": serialized_routines}))


def load_manager():
    with open("manager_store.json", "r") as file:
        output = json.loads(file.read())
        if "routines" in output and type(output["routines"]) is list:
            for serialized_routine in output["routines"]:
                r = des.deserialize_routine(serialized_routine, manager)
                if r is not None:
                    manager.add_routine(r)


load_manager()


@app.route('/', methods=["GET", "POST"])
def index():
    success = None
    if request.method == "POST":
        if "routine_name" in request.form and "card_id" in request.form:
            card_id = request.form["card_id"]
            card = manager.find_card_by_id(card_id)
            routine_name = request.form["routine_name"]
            if card is not None:
                routine = manager.find_routine(routine_name)
                if routine is not None:
                    card.link_to(routine)
                    success = "La carte \"{}\" est maintenant liée à la routine \"{}\"".format(card.name, routine.name)
                else:
                    card.unlink()
                    success = "La carte \"{}\" n'est plus liée à aucune routine".format(card.name)
                save_manager()
    return render_template("index.html", cards=manager.cards.values(), routines=manager.routines.keys(),
                           success=success)


@app.route('/card/register/', methods=["GET", "POST"])
def register_card():
    card_id = "6541564"  # TODO: Fetch card id

    if request.method == "POST":
        if card_id is None:
            return render_template("card-register.html", card_id=None, error="La carte n'est plus détectée")

        if "card_id" in request.form and "name" in request.form:
            sent_card_id = request.form["card_id"]
            if sent_card_id != str(card_id):
                return render_template("card-register.html", card_id=card_id, error="La carte a changée, recommencez")
            name = request.form["name"]
            if len(name) == 0:
                return render_template("card-register.html", card_id=card_id, error="Le nom ne doit pas être vide")
            if manager.find_card_by_name(name) is not None:
                return render_template("card-register.html", card_id=card_id, error="Ce nom est déjà utilisé")

            card = Card(card_id, name)
            manager.add_card(card)
            save_manager()

            return redirect("/")

    return render_template("card-register.html", card_id=card_id)


@app.route("/routines/", methods=["GET", "POST"])
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
                execution.ExecutionThread(r).start()
                success = "La routine s'est lancé sans erreur"
            else:
                error = "Impossible de trouver une routine avec ce nom."
        elif action == "delete":
            r = manager.find_routine(value)
            if r is not None:
                manager.remove_routine(r.name)
                save_manager()
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
                save_manager()
                success = "La routine a bien été créée."
            else:
                error = "Une routine avec ce nom existe déjà."
        elif action == "update":
            r = manager.find_routine(value)
            if r is not None:
                try:
                    task_index = request.form["task"]
                    task_index = int(task_index)
                    (t, _) = r.tasks[task_index]
                    values = {}
                    for arg_name in t.arguments:
                        arg = t.arguments[arg_name]
                        arg_value = request.form["{}Field".format(arg_name)]
                        if not validation.validate(arg, arg_value):
                            err = "La valeur {} n'est pas valide pour l'argument {}.".format(arg_value, arg_name)
                            error = err if error is None else "{} {}".format(error, err)
                        else:
                            values[arg_name] = arg_value
                    if error is None:
                        ok, error = t.on_validation(values)
                        if ok:
                            r.modify_task(task_index, values)
                            save_manager()
                            success = "La routine a bien été mise à jour."
                except KeyError:
                    error = "Une erreur est survenue"
                except ValueError:
                    error = "Une erreur est survenue"
            else:
                error = "Impossible de trouver une routine avec ce nom"
        elif action == "delete-task":
            r = manager.find_routine(value)
            if r is not None:
                try:
                    task_index = request.form["task"]
                    task_index = int(task_index)
                    r.remove_task(task_index)
                    save_manager()
                    success = "La tâche a bien été supprimée"
                except KeyError:
                    error = "Une erreur est survenue côté serveur"
                except ValueError:
                    error = "Une erreur est survenue côté serveur"
                except IndexError:
                    error = "Cette tâche n'existe pas"
            else:
                error = "Il n'existe pas de routine avec ce nom"

    return render_template("routines.html", routines=manager.routines.values(), error=error, success=success)


@app.route("/routines/add-task/<name>/")
def routine_add_task(name: str):
    r = manager.find_routine(name)
    if r is None:
        abort(404)
    return render_template("add-task.html", tasks=manager.tasks.values(), routine=r)


@app.route("/routines/add-task/<routine_name>/<task_name>/", methods=["GET", "POST"])
def routine_add_task_values(routine_name: str, task_name: str):
    r = manager.find_routine(routine_name)
    t = manager.find_task(task_name)
    if r is None or t is None:
        abort(404)

    error = None
    if request.method == "POST":
        values = {}
        for arg_name in t.arguments:
            try:
                value = request.form["%sField" % arg_name]
                if validation.validate(t.arguments[arg_name], value):
                    values[arg_name] = value
                else:
                    err = "La valeur {} n'est pas valide pour l'argument {}.".format(value, arg_name)
                    error = err if error is None else "{} {}".format(error, err)
            except KeyError:
                error = "Valeur(s) manquante(s) !"
        if error is None:
            r.add_task(t, values)
            save_manager()
            return redirect("/routines")

    return render_template("choose-args.html", routine=r, task=t, error=error)


if __name__ == '__main__':
    app.run()
