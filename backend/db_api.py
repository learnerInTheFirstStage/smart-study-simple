from database import db, User, Material, Topic, StudyPlan, DailyTask, Question, UserAnswer, TopicMastery
from datetime import datetime
import json

# 创建用户
def create_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user.user_id

# 保存上传的材料
def save_material(user_id, filename):
    material = Material(user_id=user_id, filename=filename)
    db.session.add(material)
    db.session.commit()
    return material.material_id

# 创建学习计划
def create_study_plan(user_id, material_id, topics_data, questions_by_topic):
    # 创建学习计划
    plan = StudyPlan(user_id=user_id, material_id=material_id)
    db.session.add(plan)
    db.session.flush()
    
    # 保存主题
    topic_ids = {}
    for topic_name in topics_data:
        topic = Topic(
            material_id=material_id,
            name=topic_name
        )
        db.session.add(topic)
        db.session.flush()
        topic_ids[topic_name] = topic.topic_id
    
    # 创建7天任务
    daily_tasks = []
    for day, topic_name in enumerate(list(topics_data.keys())[:7], 1):
        topic_id = topic_ids[topic_name]
        objectives = topics_data[topic_name]
        
        task = DailyTask(
            plan_id=plan.plan_id,
            day_number=day,
            topic_id=topic_id,
            objectives=objectives
        )
        db.session.add(task)
        db.session.flush()
        
        # 添加问题
        if topic_name in questions_by_topic:
            for q_data in questions_by_topic[topic_name]:
                question = Question(
                    task_id=task.task_id,
                    topic_id=topic_id,
                    question_text=q_data['question'],
                    options=json.dumps(q_data['options']),
                    correct_option=q_data['correct']
                )
                db.session.add(question)
        
        daily_tasks.append({
            'task_id': task.task_id,
            'day': day,
            'topic': topic_name,
            'objectives': objectives
        })
    
    db.session.commit()
    return plan.plan_id, daily_tasks

# 保存用户答案和更新掌握度
def save_user_answers(user_id, task_id, answers):
    task = DailyTask.query.get(task_id)
    if not task:
        return None
    
    topic_id = task.topic_id
    
    # 记录答题和计算正确率
    correct_count = 0
    total_count = len(answers)
    
    for answer in answers:
        question_id = answer.get('question_id')
        selected_option = answer.get('option')
        is_correct = answer.get('is_correct', False)
        
        if is_correct:
            correct_count += 1
        
        user_answer = UserAnswer(
            user_id=user_id,
            question_id=question_id,
            selected_option=selected_option,
            is_correct=is_correct
        )
        db.session.add(user_answer)
    
    # 更新主题掌握度
    score = correct_count / total_count if total_count > 0 else 0
    
    # 确定掌握级别
    if score >= 0.9:
        level = "mastered"
    elif score >= 0.7:
        level = "familiar"
    elif score >= 0.5:
        level = "learning"
    else:
        level = "weak"
    
    # 查找或创建掌握记录
    mastery = TopicMastery.query.filter_by(
        user_id=user_id, 
        topic_id=topic_id
    ).first()
    
    if mastery:
        mastery.mastery_level = level
        mastery.updated_at = datetime.utcnow()
    else:
        mastery = TopicMastery(
            user_id=user_id,
            topic_id=topic_id,
            mastery_level=level
        )
        db.session.add(mastery)
    
    # 标记任务完成
    task.completed = True
    
    db.session.commit()
    
    return {
        'score': score,
        'mastery_level': level
    }

# 获取用户的错题
def get_wrong_questions(user_id):
    wrong_answers = UserAnswer.query.filter_by(
        user_id=user_id, 
        is_correct=False
    ).all()
    
    result = []
    for answer in wrong_answers:
        question = Question.query.get(answer.question_id)
        if question:
            topic = Topic.query.get(question.topic_id)
            task = DailyTask.query.get(question.task_id)
            
            wrong_question = {
                'question_id': question.question_id,
                'question_text': question.question_text,
                'options': json.loads(question.options),
                'selected': answer.selected_option,
                'correct': question.correct_option,
                'topic': topic.name if topic else 'Unknown',
                'day': task.day_number if task else None
            }
            result.append(wrong_question)
    
    return result

# 获取用户的主题掌握情况
def get_topic_mastery(user_id):
    mastery_records = TopicMastery.query.filter_by(user_id=user_id).all()
    
    result = []
    for record in mastery_records:
        topic = Topic.query.get(record.topic_id)
        if topic:
            result.append({
                'topic': topic.name,
                'mastery_level': record.mastery_level,
                'updated_at': record.updated_at.strftime('%Y-%m-%d')
            })
    
    return result