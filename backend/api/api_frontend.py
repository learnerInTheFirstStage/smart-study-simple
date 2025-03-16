from flask import Flask, request, jsonify
from app import app
from db.database import db, DailyTask, StudyPlan

@app.route('/api/completed-tasks-count', methods=['GET'])
def get_completed_tasks_count():
    completed_tasks_count = DailyTask.query.filter_by(completed=True).count()
    return jsonify({"completed_tasks_count": completed_tasks_count})


@app.route('/api/daily-tasks', methods=['GET'])
def get_daily_tasks():
    # Fetch all daily tasks from the database
    daily_tasks = DailyTask.query.all()

    # Format them as a list of dictionaries to send as JSON
    result = []
    for task in daily_tasks:
        result.append({
            'id': task.id,
            'day_number': task.day_number,
            'topic_name': task.topic_name,
            'objectives': task.objectives,
            'completed': task.completed,
            'total_questions': task.total_questions,
            'wrong_count': task.wrong_count
        })

    return jsonify(result)


@app.route('/api/top-review-tasks', methods=['GET'])
def get_top_review_tasks():
    try:
        # Query the tasks sorted by wrong_count/total_questions ratio
        top_tasks = DailyTask.query.filter(DailyTask.total_questions > 0). \
            order_by((DailyTask.wrong_count / DailyTask.total_questions).desc()).limit(3).all()

        # Create a response with relevant task data
        response = [
            {
                "day_number": task.day_number,
                "topic_name": task.topic_name,
                "objectives": task.objectives,
                "wrong_count": task.wrong_count,
                "total_questions": task.total_questions
            }
            for task in top_tasks
        ]

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/study-plan', methods=['GET'])
def check_study_plan():
    # Check if there's a study plan in the database
    study_plan = StudyPlan.query.first()  # Get the first study plan (if any)

    if study_plan:
        return jsonify({"study_plan_exists": True})
    else:
        return jsonify({"study_plan_exists": False})


if __name__ == '__main__':
    app.run(debug=True)