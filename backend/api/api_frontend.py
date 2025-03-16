from flask import Flask, request, jsonify
from app import app
from db.database import db, DailyTask

@app.route('/api/completed-tasks-count', methods=['GET'])
def get_completed_tasks_count():
    completed_tasks_count = DailyTask.query.filter_by(completed=True).count()
    return jsonify({"completed_tasks_count": completed_tasks_count})


if __name__ == '__main__':
    app.run(debug=True)