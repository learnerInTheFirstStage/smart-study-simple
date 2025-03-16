import json
import requests
import re  # 导入正则表达式库，用于文本模式匹配和解析
from db.db_api import create_study_plan

api_key = "F39Y0SZ-YAMM7ZA-GQVDRSB-87E9FTJ"

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
        cleaned_text = re.sub(r"\n\nNote.*", "", text_response, flags=re.DOTALL)
        
        pattern = r"Day (\d+): (.*?)\n\"(.*?)\""
        plan_by_day = re.findall(pattern, cleaned_text)
        topics_data = []
        questions_all = []
        for _, topic, obejective in plan_by_day:
            topics_data.append({
                'Topic': topic.strip('*'),
                'Objective' : obejective.strip()
            })

            # Based on each topic, generate three multiple choice questions
            topic_prompt = f'Based on {topic}, generate three multiple choice questions, only with four options and one correct answer'
            request_body2 = {
                "message": topic_prompt,
                "mode": "chat",
            }
            question_per_topic = requests.post(url3, data=json.dumps(request_body2), headers=headers2)

            if question_per_topic.status_code == 200:
                # print(question_per_topic.json())
                row_questions = question_per_topic.json().get("documents", [{}])[0].get("textResponse", "")

                # Extract all questions
                questions = re.findall(r'(\*\*Question \d+.*?Correct answer: [A-D]\))', row_questions, re.DOTALL)

                for i, question in enumerate(questions, 1):
                    questions_all.append(question)
            create_study_plan(topics_data, title)
        return questions_all

        

    else:
        print(f'Error: Received status code {response3.status_code} - {response3.text}')
