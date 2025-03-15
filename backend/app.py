from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from api.pdf_processor import extract_text
from api.ai_handler import generate_questions, generate_study_plan

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def handle_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    text = extract_text(file_path)
    questions = generate_questions(text)
    return jsonify({'questions': questions})

@app.route('/api/submit', methods=['POST'])
def handle_submission():
    data = request.json
    score = calculate_score(data['answers'])
    study_plan = generate_study_plan(score, data['weak_areas'])
    return jsonify({'score': score, 'study_plan': study_plan})

def calculate_score(answers):
    # Implement scoring logic
    return len([a for a in answers if a['correct']]) / len(answers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)