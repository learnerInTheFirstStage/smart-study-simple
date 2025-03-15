from qualcomm.llm import load_llama
import re

model = load_llama(
    "Llama-v3.1-8B-Chat",
    device="hexagon-npu",
    quant_config="qnn-8bit"
)

def generate_questions(text, num_questions=5):
    chunk_size = 1500  # Keep under 2048 token limit
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    questions = []
    for chunk in chunks:
        prompt = f"""Generate {num_questions} multiple choice questions with 4 options and mark correct answer with (Correct).
        Example format:
        1. Question text?
        A) Option 1
        B) Option 2
        C) Option 3 (Correct)
        D) Option 4
        
        Text: {chunk}"""
        
        response = model.generate(prompt, max_tokens=500)
        questions.extend(parse_questions(response))
    
    return questions[:num_questions]

def parse_questions(text):
    pattern = r'\d+\.\s(.*?)\n(A\).*?\(Correct\)|\b)', re.DOTALL
    return [{
        'question': q[0].strip(),
        'options': [opt.strip() for opt in q[1].split('\n')],
        'correct': next((i for i, opt in enumerate(q[1].split('\n')) if '(Correct)' in opt), -1)
    } for q in re.findall(pattern, text)]

def generate_study_plan(score, weak_areas):
    prompt = f"""Create a personalized study plan for a user scoring {score*100}%.
    Focus areas: {', '.join(weak_areas)}.
    Include daily objectives and resource suggestions."""
    
    return model.generate(prompt, max_tokens=300)