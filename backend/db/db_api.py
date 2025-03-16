from db.database import db, StudyPlan, DailyTask, Question
from datetime import datetime
import json

# Study plan management functions
def create_study_plan(topics_data, filename):
    """
    Create a seven-day study plan
    
    Parameters:
    topics_data - Topic data dictionary {topic_name: learning_objective, ...}
    filename - Name of the uploaded file
    
    Returns:
    Study plan data including daily tasks
    """
    # Create study plan
    study_plan = StudyPlan(filename=filename)
    db.session.add(study_plan)
    db.session.flush()  # Get ID without committing transaction
    
    # Create daily tasks
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
            'day_number': day_number,
            'topic_name': topic_name,
            'objectives': objective
        })
        
        day_number += 1
    
    # Commit transaction
    db.session.commit()
    
    # Create response with the generated IDs now available
    response = {
        'study_plan_id': study_plan.id,
        'filename': filename,
        'daily_tasks': []
    }
    
    # Get all tasks with their generated IDs
    tasks = DailyTask.query.filter_by(study_plan_id=study_plan.id).order_by(DailyTask.day_number).all()
    for task in tasks:
        response['daily_tasks'].append({
            'task_id': task.id,
            'day_number': task.day_number,
            'topic_name': task.topic_name,
            'objectives': task.objectives
        })
    
    return response

# Question management functions
def add_questions_to_task(daily_task_id, mc_questions, fb_questions=None):
    """
    Add questions to daily task
    
    Parameters:
    daily_task_id - Task ID
    mc_questions - Multiple choice questions list [{'question': 'question text', 'options': ['option1', 'option2', ...], 'correct': correct_option_index}, ...]
    fb_questions - Fill-in-the-blank questions list [{'question': 'question text', 'answer': 'correct answer'}, ...]
    
    Returns:
    Number of questions added
    """
    # Get task
    task = DailyTask.query.get(daily_task_id)
    if not task:
        return 0
    
    count = 0
    
    # Add multiple choice questions
    for q_data in mc_questions:
        question = Question(
            daily_task_id=daily_task_id,
            question_text=q_data['question'],
            question_type='multiple_choice',
            options=json.dumps(q_data['options']),
            correct_option=q_data['correct']
        )
        db.session.add(question)
        count += 1
    
    # Add fill-in-the-blank questions
    if fb_questions:
        for q_data in fb_questions:
            question = Question(
                daily_task_id=daily_task_id,
                question_text=q_data['question'],
                question_type='fill_blank',
                correct_answer=q_data['answer']
            )
            db.session.add(question)
            count += 1
    
    db.session.commit()
    
    # Update the task's total_questions count
    task.total_questions = count
    db.session.commit()
    
    return count

def get_task_questions(daily_task_id):
    """Get all questions for a task"""
    questions = Question.query.filter_by(daily_task_id=daily_task_id).all()
    
    result = {
        'multiple_choice': [],
        'fill_blank': []
    }
    
    for q in questions:
        if q.question_type == 'multiple_choice':
            result['multiple_choice'].append({
                'id': q.id,
                'question': q.question_text,
                'options': json.loads(q.options),
                'correct': q.correct_option
            })
        else:  # fill_blank
            result['fill_blank'].append({
                'id': q.id,
                'question': q.question_text,
                'answer': q.correct_answer
            })
    
    return result

# Answer management functions
def save_user_answers(daily_task_id, mc_answers, fb_answers=None):
    """
    Save user answers and update statistics
    
    Parameters:
    daily_task_id - Task ID from database
    mc_answers - Multiple choice answers [{question_id: ID, selected_option: index}, ...]
    fb_answers - Fill-in-the-blank answers [{question_id: ID, answer: text_answer}, ...]
    
    Returns:
    Answer results statistics
    """
    # Get task information
    task = DailyTask.query.get(daily_task_id)
    if not task:
        return None
    
    # Statistics
    total = 0
    wrong_count = 0
    
    # Process multiple choice answers
    for answer_data in mc_answers:
        question_id = answer_data.get('question_id')
        selected_option = answer_data.get('selected_option')
        
        question = Question.query.get(question_id)
        if not question or question.question_type != 'multiple_choice':
            continue
        
        is_correct = (selected_option == question.correct_option)
        
        # Update question statistics
        question.times_attempted += 1
        if not is_correct:
            question.times_incorrect += 1
            wrong_count += 1
        
        total += 1
    
    # Process fill-in-the-blank answers
    if fb_answers:
        for answer_data in fb_answers:
            question_id = answer_data.get('question_id')
            text_answer = answer_data.get('answer')
            
            question = Question.query.get(question_id)
            if not question or question.question_type != 'fill_blank':
                continue
            
            # Simple check if fill-in-the-blank answer is correct
            is_correct = (text_answer.strip().lower() == question.correct_answer.strip().lower())
            
            # Update question statistics
            question.times_attempted += 1
            if not is_correct:
                question.times_incorrect += 1
                wrong_count += 1
            
            total += 1
    
    # Mark task as completed
    task.completed = True
    
    # Update task statistics
    task.total_questions = total
    task.wrong_count = wrong_count
    
    # Commit transaction
    db.session.commit()
    
    # Return results
    return {
        'task_id': daily_task_id,
        'total_questions': total,
        'wrong_count': wrong_count,
        'score': (total - wrong_count) / total if total > 0 else 0
    }

# Study plan query functions
def get_study_plan(plan_id):
    """Get complete study plan information"""
    plan = StudyPlan.query.get(plan_id)
    if not plan:
        return None
    
    # Get all daily tasks
    tasks = DailyTask.query.filter_by(study_plan_id=plan_id).order_by(DailyTask.day_number).all()
    
    daily_tasks = []
    for task in tasks:
        # Get question count
        question_count = Question.query.filter_by(daily_task_id=task.id).count()
        
        daily_tasks.append({
            'day': task.day_number,
            'task_id': task.id,
            'topic_name': task.topic_name,
            'objectives': task.objectives,
            'completed': task.completed,
            'question_count': question_count,
            'total_questions': task.total_questions,
            'wrong_count': task.wrong_count
        })
    
    return {
        'plan_id': plan.id,
        'filename': plan.filename,
        'created_at': plan.created_at.strftime('%Y-%m-%d'),
        'daily_tasks': daily_tasks
    }

# Wrong questions management functions
def get_wrong_questions(daily_task_id=None):
    """
    Get wrong questions list
    
    Parameters:
    daily_task_id - Optional, specify task ID to filter
    
    Returns:
    List of wrong questions
    """
    # Build query
    query = Question.query.filter(Question.times_incorrect > 0)
    
    # If task specified, add filter condition
    if daily_task_id:
        query = query.filter(Question.daily_task_id == daily_task_id)
    
    # Execute query
    wrong_questions = query.all()
    
    result = []
    for question in wrong_questions:
        # Get task information
        task = DailyTask.query.get(question.daily_task_id)
        
        wrong_item = {
            'question_id': question.id,
            'question_type': question.question_type,
            'question_text': question.question_text,
            'topic_name': task.topic_name if task else 'Unknown',
            'day_number': task.day_number if task else None,
            'times_attempted': question.times_attempted,
            'times_incorrect': question.times_incorrect
        }
        
        # Add type-specific information
        if question.question_type == 'multiple_choice':
            wrong_item.update({
                'options': json.loads(question.options),
                'correct_option': question.correct_option
            })
        else:  # fill_blank
            wrong_item.update({
                'correct_answer': question.correct_answer
            })
        
        result.append(wrong_item)
    
    return result

# Topic mastery management functions
def get_topic_mastery():
    """Get all topic mastery information by analyzing tasks"""
    # Get all completed tasks
    tasks = DailyTask.query.filter_by(completed=True).all()
    
    # Group by topic
    topics = {}
    for task in tasks:
        if task.topic_name not in topics:
            topics[task.topic_name] = {
                'total_questions': 0,
                'wrong_count': 0
            }
        
        topics[task.topic_name]['total_questions'] += task.total_questions
        topics[task.topic_name]['wrong_count'] += task.wrong_count
    
    # Calculate mastery levels
    result = []
    for topic_name, stats in topics.items():
        if stats['total_questions'] == 0:
            mastery_level = 'not_started'
        else:
            score = (stats['total_questions'] - stats['wrong_count']) / stats['total_questions']
            
            if score >= 0.85:
                mastery_level = "mastered"
            elif score >= 0.7:
                mastery_level = "familiar"
            elif score >= 0.5:
                mastery_level = "learning"
            else:
                mastery_level = "weak"
        
        result.append({
            'topic_name': topic_name,
            'mastery_level': mastery_level,
            'total_questions': stats['total_questions'],
            'wrong_count': stats['wrong_count']
        })
    
    return result