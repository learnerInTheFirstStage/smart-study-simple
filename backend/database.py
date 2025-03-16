from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class StudyPlan(db.Model):
    __tablename__ = 'study_plans'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    daily_tasks = db.relationship("DailyTask", back_populates="study_plan")

class DailyTask(db.Model):
    __tablename__ = 'daily_tasks'
    id = db.Column(db.Integer, primary_key=True)
    study_plan_id = db.Column(db.Integer, db.ForeignKey('study_plans.id'))
    day_number = db.Column(db.Integer, nullable=False) 
    topic_name = db.Column(db.String(100), nullable=False)  
    objectives = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    total_questions = db.Column(db.Integer, default=0)
    wrong_count = db.Column(db.Integer, default=0) 
    study_plan = db.relationship("StudyPlan", back_populates="daily_tasks")
    questions = db.relationship("Question", back_populates="daily_task")
    
class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    daily_task_id = db.Column(db.Integer, db.ForeignKey('daily_tasks.id'))
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # multiple_choice / fill_blank
    options = db.Column(db.JSON, nullable=True)  
    correct_option = db.Column(db.Integer, nullable=True) 
    correct_answer = db.Column(db.Text, nullable=True)  
    times_attempted = db.Column(db.Integer, default=0)
    times_incorrect = db.Column(db.Integer, default=0) 
    daily_task = db.relationship("DailyTask", back_populates="questions")