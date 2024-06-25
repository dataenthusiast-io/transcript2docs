from docx import Document
import webvtt
from langchain_text_splitters import TokenTextSplitter

def read_txt(file):
    return file.getvalue().decode('utf-8')

def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_vtt(file):
    vtt = webvtt.read_buffer(file)
    return "\n".join([caption.text for caption in vtt])

def split_text(text, chunk_size, chunk_overlap_ratio=0.05):
    """
    Split text into chunks for processing.
    """
    chunk_overlap = int(chunk_size * chunk_overlap_ratio)
    text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(text)