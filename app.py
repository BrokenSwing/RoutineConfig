from flask import Flask, render_template, request, abort, redirect
from api.manager import Manager
from api.task import Task
import api.arg_type as arg_type
from api.routine import Routine
from core import validation

app = Flask(__name__)
manager = Manager()
task = Task("My task")
task.register_argument("Action", arg_type.choice("Allumer", "Eteindre"))
task.register_argument("Value", arg_type.integer(minimum=0, maximum=50))
manager.register_task(task)


@app.route('/')
def index():
    return render_template("index.html")


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
                    err = "La valeur {} n'est pas valide pour l'argument {}".format(value, arg_name)
                    error = err if error is None else "{} {}".format(error, err)
            except KeyError:
                error = "Valeur(s) manquante(s) !"
        if error is None:
            r.add_task(t, values)
            return redirect("/routines")

    return render_template("choose-args.html", routine=r, task=t, error=error)


if __name__ == '__main__':
    app.run()
