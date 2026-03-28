from docling.document_converter import DocumentConverter
from pathlib import Path
from typing import Dict, Any, List
import logging


# Parser.py -> Turns files into clean, readable formatted data for LLMs to easy parae
# Handles all formats : .docx, .pdf, 

logger = logging.getLogger(__name__)

class DocumentParser:
    def __init__(self):
        self.converter = DocumentConverter()

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parses a document using Docling and returns structured content.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        logger.info(f"Parsing document: {file_path}")
        result = self.converter.convert(file_path)
        
        # Extract markdown representation and basic metadata
        content = result.document.export_to_markdown()
        
        # Basic file info
        file_info = {
            "file_name": path.name,
            "file_path": str(path.absolute()),
            "file_type": path.suffix.lower().replace(".", "")
        }
        
        return {
            "content": content,
            "file_info": file_info
        }


doc_parser = DocumentParser()
