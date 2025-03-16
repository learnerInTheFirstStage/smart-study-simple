from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    study_plan = db.relationship("StudyPlan", uselist=False, back_populates="material")

class StudyPlan(db.Model):
    __tablename__ = 'study_plans'
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    material = db.relationship("Material", back_populates="study_plan")
    daily_tasks = db.relationship("DailyTask", back_populates="study_plan")

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))
    name = db.Column(db.String(100), nullable=False)
    daily_task = db.relationship("DailyTask", uselist=False, back_populates="topic")
    questions = db.relationship("Question", back_populates="topic")

class DailyTask(db.Model):
    __tablename__ = 'daily_tasks'
    id = db.Column(db.Integer, primary_key=True)
    study_plan_id = db.Column(db.Integer, db.ForeignKey('study_plans.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    day_number = db.Column(db.Integer, nullable=False)  # 1-7
    objectives = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    study_plan = db.relationship("StudyPlan", back_populates="daily_tasks")
    topic = db.relationship("Topic", back_populates="daily_task")

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # multiple_choice / fill_blank
    options = db.Column(db.JSON, nullable=True)  # 选择题的选项
    correct_option = db.Column(db.Integer, nullable=True)  # 选择题正确索引
    correct_answer = db.Column(db.Text, nullable=True)  # 填空题正确答案
    topic = db.relationship("Topic", back_populates="questions")

class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    selected_option = db.Column(db.Integer, nullable=True)  # 选择题的选择
    text_answer = db.Column(db.Text, nullable=True)  # 填空题的回答
    is_correct = db.Column(db.Boolean, nullable=False)
    answer_time = db.Column(db.DateTime, default=datetime.utcnow)

class TopicMastery(db.Model):
    __tablename__ = 'topic_mastery'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    mastery_level = db.Column(db.String(20), nullable=False)  # mastered / familiar / learning / weak
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
