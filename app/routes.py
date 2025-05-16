from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from app.models import Task
from app import db

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
def list_tasks():
    q = Task.query

    # filter by completion status
    is_completed = request.args.get('is_completed')
    if is_completed is not None:
        val = is_completed.lower()
        if val not in ('true', 'false'):
            return jsonify({'error': "is_completed must be 'true' or 'false'"}), 400
        q = q.filter_by(is_completed=(val == 'true'))

    # filter by exact name
    name = request.args.get('name')
    if name is not None:
        q = q.filter_by(name=name)

    tasks = q.all()
    return jsonify([t.to_dict() for t in tasks]), 200

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    if not request.is_json:
        return jsonify({'error': "Invalid JSON payload"}), 400

    data = request.get_json()
    name = data.get('name')
    if not name or not isinstance(name, str) or not name.strip():
        return jsonify({'error': "Missing or empty 'name' field"}), 400

    is_completed = data.get('is_completed', False)
    if not isinstance(is_completed, bool):
        return jsonify({'error': "'is_completed' must be a boolean"}), 400

    task = Task(name=name.strip(), is_completed=is_completed)
    db.session.add(task)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': "Database error creating task"}), 400

    return jsonify(task.to_dict()), 201

@tasks_bp.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    if not request.is_json:
        return jsonify({'error': "Invalid JSON payload"}), 400

    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': f"Task with id {task_id} not found"}), 404

    data = request.get_json()

    #update task name
    if 'name' in data:
        name = data['name']
        if not name or not isinstance(name, str) or not name.strip():
            return jsonify({'error': "If provided, 'name' must be a non-empty string"}), 400
        task.name = name.strip()

    #uodate task status
    if 'is_completed' in data:
        is_completed = data['is_completed']
        if not isinstance(is_completed, bool):
            return jsonify({'error': "'is_completed' must be a boolean"}), 400
        task.is_completed = is_completed

    # none
    if not any(k in data for k in ('name', 'is_completed')):
        return jsonify({'error': "No valid field provided to update"}), 400

    db.session.commit()
    return jsonify(task.to_dict()), 200
