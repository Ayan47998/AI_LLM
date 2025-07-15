import io
from typing import Optional
import PyPDF2
import docx

from config import AppConfig


class DocumentProcessor:
    """Class to handle document processing and text extraction."""
    
    @staticmethod
    def extract_text_from_pdf(uploaded_file) -> str:
        """Extract text from PDF file."""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(uploaded_file) -> str:
        """Extract text from DOCX file."""
        try:
            doc = docx.Document(uploaded_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    @staticmethod
    def extract_text_from_txt(uploaded_file) -> str:
        """Extract text from TXT file."""
        try:
            content = uploaded_file.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            return content
        except Exception as e:
            raise Exception(f"Error reading TXT: {str(e)}")
    
    @classmethod
    def extract_text(cls, uploaded_file) -> str:
        """Extract text from uploaded file based on file type."""
        if uploaded_file is None:
            return ""
        
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return cls.extract_text_from_pdf(uploaded_file)
        elif file_extension == 'docx':
            return cls.extract_text_from_docx(uploaded_file)
        elif file_extension == 'txt':
            return cls.extract_text_from_txt(uploaded_file)
        else:
            raise Exception(f"Unsupported file format: {file_extension}")
    
    @staticmethod
    def get_supported_formats() -> list:
        """Return list of supported file formats."""
        return AppConfig.get_supported_formats()
    
    @staticmethod
    def validate_file_format(filename: str) -> bool:
        """Validate if file format is supported."""
        if not filename:
            return False
        file_extension = filename.split('.')[-1].lower()
        return file_extension in AppConfig.get_supported_formats()