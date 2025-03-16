from db.database import db, StudyPlan, DailyTask, Question
from datetime import datetime
import json

# Material Management: Saving uploaded PDF files
# Study Plan Creation: Generating a 7-day learning plan from uploaded materials
# Question Management: Creating and retrieving multiple-choice and fill-in-the-blank questions for each topic
# Answer Processing: Saving user answers and evaluating correctness
# Learning Analytics: Tracking topic mastery levels and identifying weak areas
# Wrong Answer Collection: Maintaining a list of incorrectly answered questions

# Material management functions
# def save_material(filename):
#     """Save uploaded learning material"""
#     material = Material(filename=filename)
#     db.session.add(material)
#     db.session.commit()
#     return material.material_id

# Study plan management functions
def create_study_plan(topics_data, title):
    """
    Create a seven-day study plan
    
    Parameters:
    topics_data - Topic data dictionary {topic_name: learning_objective, ...}
    
    Returns:
    Plan ID and daily tasks list
    """
    # Create study plan
    study_plan = StudyPlan(filename=title)
    db.session.add(study_plan)
    db.session.flush()  # Get ID without committing transaction
    
    # Create topics and associate daily tasks
    day_number = 1
    daily_tasks = []
    
    for topic_name, objective in topics_data.items():
        if day_number > 7:  # Only create 7 days of plan
            break
        
        # Create daily task
        daily_task = DailyTask(
            study_plan_id=study_plan.id,
            day_number=day_number,
            topic_name=topic_name,
            objectives=objective
        )
        db.session.add(daily_task)
        db.session.flush()
        
        daily_tasks.append({
            'task_id': daily_task.id,
            'day': day_number,
            'topic_name': topic_name,
            'objectives': objective
        })
        
        day_number += 1
    
    # Commit transaction
    db.session.commit()
    
    return study_plan.id, daily_tasks

# Question management functions
def add_questions_to_task(task_id, mc_questions, fb_questions):
    """
    Add questions to daily task
    
    Parameters:
    task_id - Task ID
    mc_questions - Multiple choice questions list [{'question': 'question text', 'options': ['option1', 'option2', ...], 'correct': correct_option_index}, ...]
    fb_questions - Fill-in-the-blank questions list [{'question': 'question text', 'answer': 'correct answer'}, ...]
    
    Returns:
    Number of questions added
    """
    # Get task and associated topic
    task = DailyTask.query.get(task_id)
    if not task:
        return 0
    
    count = 0
    
    # Add multiple choice questions
    for q_data in mc_questions:
        question = Question(
            task_id=task_id,
            topic_id=task.topic_id,
            question_text=q_data['question'],
            question_type='multiple_choice',
            options=json.dumps(q_data['options']),
            correct_option=q_data['correct']
        )
        db.session.add(question)
        count += 1
    
    # Add fill-in-the-blank questions
    for q_data in fb_questions:
        question = Question(
            task_id=task_id,
            topic_id=task.topic_id,
            question_text=q_data['question'],
            question_type='fill_blank',
            correct_answer=q_data['answer']
        )
        db.session.add(question)
        count += 1
    
    db.session.commit()
    return count

def get_task_questions(task_id):
    """Get all questions for a task"""
    questions = Question.query.filter_by(task_id=task_id).all()
    
    result = {
        'multiple_choice': [],
        'fill_blank': []
    }
    
    for q in questions:
        if q.question_type == 'multiple_choice':
            result['multiple_choice'].append({
                'id': q.question_id,
                'question': q.question_text,
                'options': json.loads(q.options),
                'correct': q.correct_option  # Note: In production, you might not want to return the correct answer
            })
        else:  # fill_blank
            result['fill_blank'].append({
                'id': q.question_id,
                'question': q.question_text,
                'answer': q.correct_answer  # Note: In production, you might not want to return the correct answer
            })
    
    return result

# Answer management functions
def save_user_answers(task_id, mc_answers, fb_answers):
    """
    Save user answers and update topic mastery level
    
    Parameters:
    task_id - Task ID
    mc_answers - Multiple choice answers [{question_id: ID, option: selected_option}, ...]
    fb_answers - Fill-in-the-blank answers [{question_id: ID, answer: text_answer}, ...]
    
    Returns:
    Answer results statistics
    """
    # Get task information
    task = DailyTask.query.get(task_id)
    if not task:
        return None
    
    # Statistics
    total = 0
    correct = 0
    mc_total = 0
    mc_correct = 0
    fb_total = 0
    fb_correct = 0
    
    # Process multiple choice answers
    for answer_data in mc_answers:
        question_id = answer_data.get('question_id')
        selected_option = answer_data.get('option')
        
        question = Question.query.get(question_id)
        if not question or question.question_type != 'multiple_choice':
            continue
        
        is_correct = (selected_option == question.correct_option)
        
        # Save answer
        answer = UserAnswer(
            question_id=question_id,
            selected_option=selected_option,
            is_correct=is_correct
        )
        db.session.add(answer)
        
        # Update statistics
        total += 1
        mc_total += 1
        if is_correct:
            correct += 1
            mc_correct += 1
    
    # Process fill-in-the-blank answers
    for answer_data in fb_answers:
        question_id = answer_data.get('question_id')
        text_answer = answer_data.get('answer')
        
        question = Question.query.get(question_id)
        if not question or question.question_type != 'fill_blank':
            continue
        
        # Simple check if fill-in-the-blank answer is correct (can use more complex matching logic if needed)
        is_correct = (text_answer.strip().lower() == question.correct_answer.strip().lower())
        
        # Save answer
        answer = UserAnswer(
            question_id=question_id,
            text_answer=text_answer,
            is_correct=is_correct
        )
        db.session.add(answer)
        
        # Update statistics
        total += 1
        fb_total += 1
        if is_correct:
            correct += 1
            fb_correct += 1
    
    # Update topic mastery level
    score = correct / total if total > 0 else 0
    
    # Determine mastery level based on score
    if score >= 0.85:
        mastery_level = "mastered"
    elif score >= 0.7:
        mastery_level = "familiar"
    elif score >= 0.5:
        mastery_level = "learning"
    else:
        mastery_level = "weak"
    
    # Update or create mastery record
    mastery = TopicMastery.query.filter_by(
        topic_id=task.topic_id
    ).first()
    
    if mastery:
        mastery.mastery_level = mastery_level
        mastery.updated_at = datetime.utcnow()
    else:
        mastery = TopicMastery(
            topic_id=task.topic_id,
            mastery_level=mastery_level
        )
        db.session.add(mastery)
    
    # Mark task as completed
    task.completed = True
    
    # Commit transaction
    db.session.commit()
    
    # Return results
    return {
        'task_id': task_id,
        'topic_id': task.topic_id,
        'topic_name': Topic.query.get(task.topic_id).name,
        'total_questions': total,
        'correct_answers': correct,
        'score': score,
        'mastery_level': mastery_level,
        'multiple_choice': {
            'total': mc_total,
            'correct': mc_correct
        },
        'fill_blank': {
            'total': fb_total,
            'correct': fb_correct
        }
    }

# Study plan query functions
def get_study_plan(plan_id):
    """Get complete study plan information"""
    plan = StudyPlan.query.get(plan_id)
    if not plan:
        return None
    
    # Get material information
    material = Material.query.get(plan.material_id)
    
    # Get all daily tasks
    tasks = DailyTask.query.filter_by(plan_id=plan_id).order_by(DailyTask.day_number).all()
    
    daily_tasks = []
    for task in tasks:
        # Get topic information
        topic = Topic.query.get(task.topic_id)
        
        # Get question count
        question_count = Question.query.filter_by(task_id=task.task_id).count()
        
        # Get topic mastery level
        mastery = TopicMastery.query.filter_by(
            topic_id=task.topic_id
        ).first()
        
        daily_tasks.append({
            'day': task.day_number,
            'task_id': task.task_id,
            'topic': topic.name,
            'objectives': task.objectives,
            'completed': task.completed,
            'question_count': question_count,
            'mastery_level': mastery.mastery_level if mastery else 'not_started'
        })
    
    return {
        'plan_id': plan.plan_id,
        'material': material.filename,
        'created_at': plan.created_at.strftime('%Y-%m-%d'),
        'daily_tasks': daily_tasks
    }

# Wrong questions management functions
def get_wrong_questions(topic_id=None):
    """
    Get wrong questions list
    
    Parameters:
    topic_id - Optional, specify topic ID to filter
    
    Returns:
    List of wrong questions
    """
    # Build query
    query = UserAnswer.query.filter_by(is_correct=False)
    
    # If topic specified, add filter condition
    if topic_id:
        query = query.join(Question).filter(Question.topic_id == topic_id)
    
    # Execute query
    wrong_answers = query.order_by(UserAnswer.answer_time.desc()).all()
    
    result = []
    for answer in wrong_answers:
        question = Question.query.get(answer.question_id)
        if not question:
            continue
        
        # Get topic information
        topic = Topic.query.get(question.topic_id)
        
        # Get task information
        task = DailyTask.query.get(question.task_id)
        
        wrong_item = {
            'question_id': question.question_id,
            'question_type': question.question_type,
            'question_text': question.question_text,
            'topic': topic.name if topic else 'Unknown',
            'day': task.day_number if task else None,
            'answer_time': answer.answer_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add type-specific information
        if question.question_type == 'multiple_choice':
            wrong_item.update({
                'options': json.loads(question.options),
                'selected_option': answer.selected_option,
                'correct_option': question.correct_option
            })
        else:  # fill_blank
            wrong_item.update({
                'user_answer': answer.text_answer,
                'correct_answer': question.correct_answer
            })
        
        result.append(wrong_item)
    
    return result

# Topic mastery management functions
def get_topic_mastery():
    """Get all topic mastery information"""
    mastery_records = TopicMastery.query.all()
    
    result = []
    for record in mastery_records:
        topic = Topic.query.get(record.topic_id)
        if not topic:
            continue
            
        result.append({
            'topic_id': record.topic_id,
            'topic_name': topic.name,
            'mastery_level': record.mastery_level,
            'updated_at': record.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return result