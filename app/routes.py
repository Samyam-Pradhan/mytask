from flask import Blueprint, request, jsonify
from . import db
from .models import Task

main = Blueprint('main', __name__)

# Health check (important for DevOps later)
@main.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# ✅ Create Task
@main.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_task = Task(title=data["title"])
    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201


# ✅ Get All Tasks
@main.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


# ✅ Get Single Task
@main.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())


# ✅ Update Task
@main.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()

    if "title" in data:
        task.title = data["title"]
    if "completed" in data:
        task.completed = data["completed"]

    db.session.commit()

    return jsonify(task.to_dict())


# ✅ Delete Task
@main.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted"})