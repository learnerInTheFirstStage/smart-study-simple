import requests
import json
import re

url = "http://localhost:3001/api/v1/document/upload"
# url2 = "http://localhost:3001/api/v1/documents"
slug = "llm"
url3 = f'http://localhost:3001/api/v1/workspace/{slug}/chat'
api_key = "F39Y0SZ-YAMM7ZA-GQVDRSB-87E9FTJ"
pdf_file_path = "CommandLine.pdf"  # Replace with your PDF file path

# Prepare the file payload
files = {
    'file': ('CommandLine.pdf', open(pdf_file_path, 'rb'), 'application/pdf')
}

# Add the A PI key in headers
headers = {
    'accept': "application/json",
    'Authorization': f'Bearer {api_key}'
}


# Send the POST request
response = requests.post(url, files=files, headers=headers)
# response2 = requests.get(url2, headers=headers)

# Check the response
if response.status_code == 200:
    print("Upload successful!")

    # Parse the JSON response
    response_json = response.json()
    
    # Extract the pageContent and wordCount
    title = response_json.get("documents", [{}])[0].get("title", "").split('.')[0]
    content = response_json.get("documents", [{}])[0].get("pageContent", "").strip()

    print("Title: ", title)
    
    # Check if content exists and is non-empty
    if content:
        print("Content Length :", len(content))
    else:
        print("No Page Content found.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# if response2.status_code == 200:
#     print(response2.json())
 
new_message = f'Based on the following content, {content}, generate a 7-day study plan for learning it, just containing day number, topic and one simple sentence of how to learn, no any other things in textRespond field'
request_body = {
    "message": new_message,
    "mode": "chat",
}

headers2 = {
    'accept': "application/json",
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

response3 = requests.post(url3, data=json.dumps(request_body), headers=headers2)

if response3.status_code == 200:
    # print("Response from API", response3.json())
    # Extract the 'textResponse' content
    text_response = response3.json().get('textResponse', '')

    # Remove the final paragraph
    cleaned_text = re.sub(r"\n\nNote.*", "", text_response, flags=re.DOTALL)

    # Extract the Study Plan
    # study_plan_match = re.search(r'(?<=\*\*7-Day Study Plan:\*\*\n)([\s\S]+)', text_response)
    # study_plan = study_plan_match.group(1).strip() if study_plan_match else "Study Plan not found"

    # print("Topic:", topic)
    # print("\nStudy Plan:")
    # print(study_plan)
    

    # Extract study plan details
    # days = re.split(r'(\*\*Day \d+: .*?\*\*)', cleaned_text)
    
    # Combine headers with their respective content
    # study_plan_by_day = {
    #     days[i].strip('* ').strip(): days[i + 1].strip() for i in range(1, len(days) - 1, 2)
    # }

    # Display each day's study plan
    # for day, content in study_plan_by_day.items():
    #     print(f"{day}\n{content}\n{'-'*40}")

    print(cleaned_text)
    pattern = r"\*\*Day (\d+): (.*?)\*\*\s*(.*?)\s*(?=\*\*Day|\Z)"
    plan_per_day = re.findall(pattern, cleaned_text, re.DOTALL)
    print('Plan per day:', plan_per_day)
    topics_data = []
    for _, topic, obejective in plan_per_day:
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
                print(f"Question {i}:\n{question.strip()}\n")

else:
    print(f'Error: Received status code {response3.status_code} - {response3.text}')