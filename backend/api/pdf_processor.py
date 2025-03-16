import fitz  # PyMuPDF，一个强大的PDF处理库
import re    # 正则表达式库，用于文本处理
import logging  # 日志记录
from typing import List, Tuple  # 类型注解，提高代码可读性

# 配置日志系统
logging.basicConfig(level=logging.INFO)  # 设置日志级别为INFO
logger = logging.getLogger(__name__)  # 获取当前模块的logger

class PDFProcessingError(Exception):
    """自定义PDF处理异常类，用于更精确地表示PDF处理过程中的错误"""
    pass

def extract_text(pdf_path: str, chunk_size: int = 1500, overlap: int = 200) -> List[Tuple[int, str]]:
    """
    提取PDF文本并进行智能分块
    
    参数:
        pdf_path (str): PDF文件路径
        chunk_size (int): 每个文本块的最大长度（字符数）
        overlap (int): 分块重叠区域大小（字符数），用于保持上下文连贯性
        
    返回:
        List[Tuple[int, str]]: 包含（页码，文本块）的列表
        
    异常:
        PDFProcessingError: 处理失败时抛出
    """
    try:
        doc = fitz.open(pdf_path)  # 打开PDF文档
        full_text = []  # 存储提取的文本和页码
        
        # 逐页提取文本并保留结构信息
        for page_num, page in enumerate(doc):
            text = page.get_text("blocks")  # 以块为单位获取文本，保留文档结构
            # 只保留类型为文本的块，类型标识为0的是文本块，用换行符连接
            page_text = "\n".join([block[4] for block in text if block[6] == 0])
            
            # 智能分页处理：如果页面文本超过设定的chunk_size，进行分块
            if len(page_text) > chunk_size:
                chunks = smart_chunk(page_text, chunk_size, overlap)  # 调用智能分块函数
                full_text.extend([(page_num+1, chunk) for chunk in chunks])  # 将分块结果加入列表，页码从1开始
            else:
                full_text.append((page_num+1, page_text))  # 页面文本不需要分块，直接添加
        
        # 合并太小的文本块，提高处理效率
        return merge_small_chunks(full_text, min_size=500)
    
    except fitz.FileDataError as e:
        # 捕获PDF文件损坏或格式错误的异常
        logger.error(f"PDF文件损坏: {str(e)}")
        raise PDFProcessingError("无效的PDF文件格式") from e
    except Exception as e:
        # 捕获其他所有异常
        logger.error(f"PDF处理失败: {str(e)}")
        raise PDFProcessingError("无法处理PDF文件") from e

def smart_chunk(text: str, chunk_size: int, overlap: int) -> List[str]:
    """
    基于段落和句子的智能分块
    
    将文本智能地分割成块，尊重段落和句子边界，确保语义连贯性
    
    参数:
        text: 要分块的文本
        chunk_size: 每块的最大字符数
        overlap: 块之间的重叠字符数
        
    返回:
        分块后的文本列表
    """
    chunks = []  # 存储最终的分块结果
    current_chunk = []  # 当前正在构建的块
    current_length = 0  # 当前块的累计长度
    
    # 按段落分割文本
    paragraphs = re.split(r'\n\s*\n', text)  # 使用空行作为段落分隔符
    
    for para in paragraphs:
        para = para.strip()  # 去除段落前后的空白
        if not para:
            continue  # 跳过空段落
            
        # 如果添加当前段落会使当前块超过最大长度
        if current_length + len(para) > chunk_size:
            # 处理超长段落（段落本身就超过chunk_size）
            if len(para) > chunk_size:
                # 按句子分割段落
                sentences = re.split(r'(?<=[.!?])\s+', para)  # 在句号、感叹号、问号后面跟空格的位置分割
                for sent in sentences:
                    # 如果添加当前句子会使当前块超过最大长度
                    if current_length + len(sent) > chunk_size:
                        if current_chunk:
                            # 将当前块添加到结果中
                            chunks.append("\n".join(current_chunk))
                            # 保留一部分上下文作为新块的开始，overlap/50是一个启发式值
                            current_chunk = current_chunk[-int(overlap/50):]
                            current_length = sum(len(s) for s in current_chunk)
                        # 将当前句子添加到块中
                        current_chunk.append(sent)
                        current_length += len(sent)
                    else:
                        # 句子可以放入当前块
                        current_chunk.append(sent)
                        current_length += len(sent)
            else:
                # 段落不超长，但加入会超过chunk_size，结束当前块
                chunks.append("\n".join(current_chunk))
                # 开始新块
                current_chunk = [para]
                current_length = len(para)
        else:
            # 段落可以放入当前块
            current_chunk.append(para)
            current_length += len(para)
    
    # 处理最后一个块
    if current_chunk:
        chunks.append("\n".join(current_chunk))
    
    return chunks

def merge_small_chunks(chunks: List[Tuple[int, str]], min_size: int = 300) -> List[Tuple[int, str]]:
    """
    合并过小的文本块以优化处理
    
    参数:
        chunks: 包含(页码,文本)的列表
        min_size: 最小块大小阈值，小于此值的块将尝试合并
        
    返回:
        合并后的块列表
    """
    merged = []  # 存储合并后的结果
    current_page = None  # 当前处理的页码
    current_text = []  # 当前累积的小块文本
    
    for page_num, text in chunks:
        if len(text) < min_size:  # 如果文本块小于最小大小
            if current_page is None:
                current_page = page_num  # 记录第一个小块的页码
            current_text.append(text)  # 添加到待合并列表
        else:
            # 处理文本块足够大的情况
            if current_text:  # 如果有待合并的小块
                # 合并之前累积的小块
                merged.append((current_page, "\n".join(current_text)))
                current_text = []  # 重置
            # 添加当前足够大的块
            merged.append((page_num, text))
    
    # 处理最后剩余的小块
    if current_text:
        merged.append((current_page, "\n".join(current_text)))
    
    return merged