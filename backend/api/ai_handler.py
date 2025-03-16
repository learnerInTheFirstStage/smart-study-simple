import json
import requests
import re  # 导入正则表达式库，用于文本模式匹配和解析

api_key = "F39Y0SZ-YAMM7ZA-GQVDRSB-87E9FTJ"

def generate_questions(text, num_questions=5):
    """
    从给定文本生成多项选择题
    
    参数:
        text: 源文本内容
        num_questions: 要生成的问题数量，默认为5个
    
    返回:
        问题列表，每个问题包含问题文本、选项和正确答案索引
    """
    chunk_size = 1500  # 文本块大小，保持在2048 token限制以下
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]  # 将文本分割成小块
    
    questions = []
    for chunk in chunks:
        # 构建提示词，指导LLM生成特定格式的问题
        prompt = f"""Generate {num_questions} multiple choice questions with 4 options and mark correct answer with (Correct).
        Example format:
        1. Question text?
        A) Option 1
        B) Option 2
        C) Option 3 (Correct)
        D) Option 4
        
        Text: {chunk}"""
        
        # 使用模型生成问题，限制最大输出token数为500
        response = model.generate(prompt, max_tokens=500)
        # 解析生成的文本，提取问题和选项
        questions.extend(parse_questions(response))
    
    # 返回指定数量的问题（如果生成的问题超过了要求的数量，只返回前num_questions个）
    return questions[:num_questions]

def parse_questions(text):
    """
    解析模型生成的文本，提取格式化的问题、选项和正确答案
    
    参数:
        text: 模型生成的包含问题和选项的文本
    
    返回:
        解析后的问题列表，每个问题是包含问题文本、选项和正确答案索引的字典
    """
    # 正则表达式模式，用于匹配问题和选项
    pattern = r'\d+\.\s(.*?)\n(A\).*?\(Correct\)|\b)', re.DOTALL
    
    # 使用列表推导式处理找到的所有问题
    return [{
        'question': q[0].strip(),  # 问题文本，去除前后空白
        'options': [opt.strip() for opt in q[1].split('\n')],  # 选项列表，每个选项去除前后空白
        'correct': next((i for i, opt in enumerate(q[1].split('\n')) if '(Correct)' in opt), -1)  # 找出标记为正确的选项索引
    } for q in re.findall(pattern, text)]  # 对文本中匹配到的每个问题执行操作

def generate_study_plan(file):
    # 构建提示词，指导模型生成学习计划
    url = "http://localhost:3001/api/v1/document/upload"
    slug = "llm"
    url3 = f'http://localhost:3001/api/v1/workspace/{slug}/chat'
    files = {'file': (file.filename, file.stream, 'application/pdf')}

    # Add the A PI key in headers
    headers = {
        'accept': "application/json",
        'Authorization': f'Bearer {api_key}'
    }
    
    # Send the POST request
    response = requests.post(url, files=files, headers=headers)

    if response.status_code == 200:
        print("Upload successful!")

        # Parse the JSON response
        response_json = response.json()
        
        # Extract the pageContent and wordCount
        title = response_json.get("documents", [{}])[0].get("title", "").split('.')[0]
        content = response_json.get("documents", [{}])[0].get("pageContent", "").strip()
    
        # Check if content exists and is non-empty
        if content:
            print("Content Length :", len(content))
        else:
            print("No Page Content found.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    
    prompt = f'Based on the following content, {content}, generate a 7-day study plan for learning it, just containing day number, topic and one simple sentence of how to learn'
    request_body = {
    "message": prompt,
    "mode": "chat",
    }
    
    headers2 = {
    'accept': "application/json",
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
    }

    response3 = requests.post(url3, data=json.dumps(request_body), headers=headers2)

    if response3.status_code == 200:
        text_response = response3.json().get('textResponse', '')
        
        # Extract study plan details
        days = re.split(r'(\*\*Day \d+: .*?\*\*)', text_response)
        
        # Combine headers with their respective content
        study_plan_by_day = {
        days[i].strip('* ').strip(): days[i + 1].strip() for i in range(1, len(days) - 1, 2)
        }

    else:
        print(f'Error: Received status code {response3.status_code} - {response3.text}')

# Receive message returned by the model, turn it into the plan json file, 
# pass it to the db part: 
    # Parameters needed:
    #     material_id - Material ID
    #     topics_data - Topic data dictionary {topic_name: learning_objective, ...}
# AI暂定以下格式返回：string格式
# 1
# read 20 pages
# do 30 practice problems
# ...
def initialize_studyplan(prompt):
    # Send prompt to AI model
    prompt = "Give me a plan"
    ai_generated_plan = model.generate(prompt)
    
    # Parse the AI response
    # First, split the response into lines
    lines = ai_generated_plan.strip().split('\n')
    
    # Extract the material ID (first element)
    try:
        material_id = int(lines[0].strip())
    except (ValueError, IndexError):
        # Handle case where material_id is not a valid integer
        material_id = None
    
    # Extract the daily tasks (remaining elements)
    daily_tasks = []
    for line in lines[1:]:
        if line.strip():  # Skip empty lines
            daily_tasks.append(line.strip())
    
    # Return structured plan
    return {
        "material_id": material_id,
        "daily_tasks": daily_tasks
    }