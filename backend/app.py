# 导入必要的库
from flask import Flask, request, jsonify  # Flask框架核心组件
from flask_cors import CORS  # 处理跨域资源共享(CORS)
import os  # 操作系统相关功能
from api.pdf_processor import extract_text  # 自定义PDF文本提取模块
from api.ai_handler import generate_questions, generate_study_plan  # AI生成问题和学习计划的模块

# 创建Flask应用实例
app = Flask(__name__)
CORS(app)  # 启用CORS，允许来自不同域的前端访问这个API

# 设置上传文件夹
UPLOAD_FOLDER = 'uploads'  # 定义上传文件的存储路径
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 确保上传文件夹存在，如不存在则创建

# 定义文件上传API端点
@app.route('/api/upload', methods=['POST'])  # 指定路由路径和HTTP方法
def handle_upload():
    # 检查请求中是否包含文件
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400  # 如果没有文件，返回400错误
    
    # 获取上传的文件
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)  # 构建文件存储路径
    file.save(file_path)  # 保存文件到服务器
    
    # 处理上传的文件
    text = extract_text(file_path)  # 提取PDF文本内容
    questions = generate_questions(text)  # 基于提取的文本生成问题
    return jsonify({'questions': questions})  # 返回生成的问题作为JSON响应

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
        port=5000,       # 在端口5000上运行
        threaded=True    # 启用多线程处理请求
    )