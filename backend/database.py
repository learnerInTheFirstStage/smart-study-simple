from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 用户表：user_id主键，用户名、电子邮件、创建时间
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 材料表：material_id主键，文件名，上传日期
class Material(db.Model):
    __tablename__ = 'materials'
    material_id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

# 主题表：topic_id主键，关联的材料ID，主题名称
class Topic(db.Model):
    __tablename__ = 'topics'
    topic_id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'))
    name = db.Column(db.String(100), nullable=False)

# 学习计划表：plan_id主键，用户ID，材料ID，创建时间
class StudyPlan(db.Model):
    __tablename__ = 'study_plans'
    plan_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 每日学习任务表：task_id主键，计划ID，天数，关联的主题ID，任务目标，完成状态
class DailyTask(db.Model):
    __tablename__ = 'daily_tasks'
    task_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('study_plans.plan_id'))
    day_number = db.Column(db.Integer, nullable=False)  # 1-7
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'))
    objectives = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)

# 问题表：question_id主键，任务ID，主题ID，问题文本，问题类别（填空/选择），正确答案
class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('daily_tasks.task_id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'))
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # "multiple_choice" 或 "fill_blank"
    
    # 选择题的选项和正确答案
    options = db.Column(db.JSON, nullable=True)  # 选择题的选项数组，填空题为null
    correct_option = db.Column(db.Integer, nullable=True)  # 选择题的正确选项索引，填空题为null
    
    # 填空题的正确答案
    correct_answer = db.Column(db.Text, nullable=True)  # 填空题的正确答案，选择题为null

# 用户答题表：answer_id主键，用户ID，问题ID，选择的选项，是否正确，答题时间
class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    answer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    # 选择题的答案
    selected_option = db.Column(db.Integer, nullable=True)  # 选择题的选择，填空题为null
    # 填空题的答案
    text_answer = db.Column(db.Text, nullable=True)  # 填空题的回答，选择题为null
    is_correct = db.Column(db.Boolean, nullable=False)
    answer_time = db.Column(db.DateTime, default=datetime.utcnow)

# 主题掌握度表：mastery_id主键，用户ID，主题ID，掌握程度，更新时间
class TopicMastery(db.Model):
    __tablename__ = 'topic_mastery'
    mastery_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'))
    # 掌握程度: "mastered", "familiar", "learning", "weak"
    mastery_level = db.Column(db.String(20), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)