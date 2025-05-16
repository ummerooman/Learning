from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

# flask and db
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'tasks.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'  # point to sqlite file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # created an SQLAlchemy object db with app instance

# model
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_completed': self.is_completed
        }

# create db & table
with app.app_context():
    db.create_all()

# routes
@app.route('/tasks', methods=['GET'])
def list_tasks():
    q = Task.query
    # filter by is_completed if provided
    is_completed = request.args.get('is_completed')
    if is_completed is not None:
        val = is_completed.lower()
        if val not in ('true', 'false'):
            return jsonify({'error': "is_completed must be 'true' or 'false'"}), 400
        q = q.filter_by(is_completed=(val == 'true'))
    # filter by exact name if provided
    name = request.args.get('name')
    if name is not None:
        q = q.filter_by(name=name)
    tasks = q.all()
    return jsonify([t.to_dict() for t in tasks]), 200

@app.route('/tasks', methods=['POST'])
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

@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    if not request.is_json:
        return jsonify({'error': "Invalid JSON payload"}), 400
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': f"Task with id {task_id} not found"}), 404
    data = request.get_json()
    if 'name' in data:
        name = data['name']
        if not name or not isinstance(name, str) or not name.strip():
            return jsonify({'error': "If provided, 'name' must be a non-empty string"}), 400
        task.name = name.strip()
    if 'is_completed' in data:
        is_completed = data['is_completed']
        if not isinstance(is_completed, bool):
            return jsonify({'error': "'is_completed' must be a boolean"}), 400
        task.is_completed = is_completed
    # nothing to update?
    if not any(k in data for k in ('name', 'is_completed')):
        return jsonify({'error': "No valid field provided to update"}), 400
    db.session.commit()
    return jsonify(task.to_dict()), 200

if __name__ == '__main__':
    app.run(debug=True)
