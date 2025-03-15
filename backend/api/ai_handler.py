# 导入必要的库
from qualcomm.llm import load_llama  # 导入高通提供的LLaMA模型加载函数
import re  # 导入正则表达式库，用于文本模式匹配和解析

# 加载LLaMA模型
model = load_llama(
    "Llama-v3.1-8B-Chat",  # 指定使用LLaMA 3.1 8B参数的聊天模型
    device="hexagon-npu",   # 在高通Hexagon NPU（神经处理单元）上运行
    quant_config="qnn-8bit" # 使用8位量化配置以减少内存占用和提高推理速度
)

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

def generate_study_plan(score, weak_areas):
    """
    基于用户得分和弱点领域生成个性化学习计划
    
    参数:
        score: 用户得分（0-1之间的小数）
        weak_areas: 需要加强的领域列表
    
    返回:
        生成的学习计划文本
    """
    # 构建提示词，指导模型生成学习计划
    prompt = f"""Create a personalized study plan for a user scoring {score*100}%.
    Focus areas: {', '.join(weak_areas)}.
    Include daily objectives and resource suggestions."""
    
    # 使用模型生成学习计划，限制最大输出token数为300
    return model.generate(prompt, max_tokens=300)