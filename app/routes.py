from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from . import db
from .models import Task

main = Blueprint('main', __name__)

@main.route("/")
def home():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)


@main.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")

    if title:
        new_task = Task(title=title)
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for("main.home"))

@main.route("/toggle/<int:id>")
def toggle_task(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("main.home"))


@main.route("/delete/<int:id>")
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("main.home"))

@main.route("/api/tasks")
def api_tasks():
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks])