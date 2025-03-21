# 导入必要的库
from flask import Flask, request, jsonify  # Flask框架核心组件
from flask_cors import CORS  # 处理跨域资源共享(CORS)
import os  # 操作系统相关功能
# from api.pdf_processor import extract_text  # 自定义PDF文本提取模块
from api.ai_handler import  generate_study_plan  # AI生成问题和学习计划的模块

# Import database models
from db.database import db
from db.db_api import (
    create_study_plan, add_questions_to_task, 
    get_task_questions, save_user_answers, get_wrong_questions,
    get_study_plan, get_topic_mastery
)
from db.db_init import init_db

from api.api_frontend import register_routes

app = Flask(__name__)
CORS(app)  # 启用CORS，允许来自不同域的前端访问这个API
init_db(app)
register_routes(app)
# # 设置上传文件夹
# UPLOAD_FOLDER = 'uploads'  # 定义上传文件的存储路径
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 确保上传文件夹存在，如不存在则创建

# 定义文件上传API端点
@app.route('/api/upload', methods=['POST'])  # 指定路由路径和HTTP方法
def handle_upload():
    # 检查请求中是否包含文件
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400  # 如果没有文件，返回400错误
    
    file = request.files['file']
    
    questions_all = generate_study_plan(file)
    return jsonify({'questions': questions_all})  # 返回生成的问题作为JSON响应

# 定义提交答案API端点
@app.route('/api/submit', methods=['POST'])
def handle_submission():
    data = request.json  # 获取JSON格式的请求数据
    score = calculate_score(data['answers'])  # 计算答案得分
    study_plan = generate_study_plan(score, data['weak_areas'])  # 根据得分和弱点生成学习计划
    return jsonify({'score': score, 'study_plan': study_plan})  # 返回得分和学习计划

# 计算得分的辅助函数
def calculate_score(answers):
    # 计算正确答案的比例作为分数
    # 使用列表推导式找出所有正确的答案，然后除以总答案数
    return len([a for a in answers if a['correct']]) / len(answers)

# 程序入口点
if __name__ == '__main__':
    # 启动Flask应用服务器
    app.run(
        host='0.0.0.0',  # 监听所有可用的网络接口
        port=5001,       # 在端口5000上运行
        threaded=True    # 启用多线程处理请求
    )