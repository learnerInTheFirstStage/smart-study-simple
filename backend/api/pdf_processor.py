import fitz  # PyMuPDF
import re
import logging
from typing import List, Tuple

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessingError(Exception):
    """自定义PDF处理异常"""
    pass

def extract_text(pdf_path: str, chunk_size: int = 1500, overlap: int = 200) -> List[Tuple[int, str]]:
    """
    提取PDF文本并进行智能分块
    
    参数:
        pdf_path (str): PDF文件路径
        chunk_size (int): 每个文本块的最大长度（字符数）
        overlap (int): 分块重叠区域大小（字符数）
        
    返回:
        List[Tuple[int, str]]: 包含（页码，文本块）的列表
        
    异常:
        PDFProcessingError: 处理失败时抛出
    """
    try:
        doc = fitz.open(pdf_path)
        full_text = []
        
        # 提取文本并保留结构信息
        for page_num, page in enumerate(doc):
            text = page.get_text("blocks")  # 获取文本块
            page_text = "\n".join([block[4] for block in text if block[6] == 0])  # 0=文本
            
            # 智能分页处理
            if len(page_text) > chunk_size:
                chunks = smart_chunk(page_text, chunk_size, overlap)
                full_text.extend([(page_num+1, chunk) for chunk in chunks])
            else:
                full_text.append((page_num+1, page_text))
        
        return merge_small_chunks(full_text, min_size=500)
    
    except fitz.FileDataError as e:
        logger.error(f"PDF文件损坏: {str(e)}")
        raise PDFProcessingError("无效的PDF文件格式") from e
    except Exception as e:
        logger.error(f"PDF处理失败: {str(e)}")
        raise PDFProcessingError("无法处理PDF文件") from e

def smart_chunk(text: str, chunk_size: int, overlap: int) -> List[str]:
    """基于段落和句子的智能分块"""
    chunks = []
    current_chunk = []
    current_length = 0
    
    # 按段落分割
    paragraphs = re.split(r'\n\s*\n', text)
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        if current_length + len(para) > chunk_size:
            # 处理超长段落
            if len(para) > chunk_size:
                sentences = re.split(r'(?<=[.!?])\s+', para)
                for sent in sentences:
                    if current_length + len(sent) > chunk_size:
                        if current_chunk:
                            chunks.append("\n".join(current_chunk))
                            current_chunk = current_chunk[-int(overlap/50):]  # 保留部分上下文
                            current_length = sum(len(s) for s in current_chunk)
                        current_chunk.append(sent)
                        current_length += len(sent)
                    else:
                        current_chunk.append(sent)
                        current_length += len(sent)
            else:
                chunks.append("\n".join(current_chunk))
                current_chunk = [para]
                current_length = len(para)
        else:
            current_chunk.append(para)
            current_length += len(para)
    
    if current_chunk:
        chunks.append("\n".join(current_chunk))
    
    return chunks

def merge_small_chunks(chunks: List[Tuple[int, str]], min_size: int = 300) -> List[Tuple[int, str]]:
    """合并过小的文本块"""
    merged = []
    current_page = None
    current_text = []
    
    for page_num, text in chunks:
        if len(text) < min_size:
            if current_page is None:
                current_page = page_num
            current_text.append(text)
        else:
            if current_text:
                merged.append((current_page, "\n".join(current_text)))
                current_text = []
            merged.append((page_num, text))
    
    if current_text:
        merged.append((current_page, "\n".join(current_text)))
    
    return merged