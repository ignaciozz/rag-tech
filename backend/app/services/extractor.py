import io
from typing import List, Dict, Any
from pypdf import PdfReader
from docx import Document as DocxDocument

def extract_text_from_txt_or_md(file_bytes: bytes) -> List[Dict[str, Any]]:
    """
    Extrai texto de arquivos de texto puro (.txt ou .md).
    Como não há páginas fixas, consideramos todo o conteúdo como página 1.
    """
    # TODO 1: Decodifique os bytes recebidos para string usando UTF-8 (com fallback para 'ignore' se houver caractere estranho)
    # Dica: text = file_bytes.decode("utf-8", errors="ignore")
    # Retorne no formato: [{"page_number": 1, "text": text.strip()}]
    pass


def extract_text_from_pdf(file_bytes: bytes) -> List[Dict[str, Any]]:
    """
    Extrai o texto página por página de um arquivo PDF usando o pypdf.
    """
    pages_content: List[Dict[str, Any]] = []
    
    # Cria um leitor de PDF a partir dos bytes na memória
    pdf_file = io.BytesIO(file_bytes)
    reader = PdfReader(pdf_file)

    # TODO 2: Percorra as páginas do PDF com enumerate(reader.pages, start=1)
    # 1. Obtenha o texto da página usando: page.extract_text()
    # 2. Se o texto não estiver vazio, adicione ao pages_content:
    #    pages_content.append({"page_number": page_num, "text": text.strip()})
    
    return pages_content


def extract_text_from_docx(file_bytes: bytes) -> List[Dict[str, Any]]:
    """
    Extrai texto de arquivos Word (.docx).
    """
    doc_file = io.BytesIO(file_bytes)
    doc = DocxDocument(doc_file)
    
    full_text = "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
    
    return [{"page_number": 1, "text": full_text.strip()}]


def extract_text(file_bytes: bytes, file_type: str) -> List[Dict[str, Any]]:
    """
    Função principal (Dispatcher) que escolhe o extrator correto
    baseado na extensão do arquivo.
    """
    file_type = file_type.lower().replace(".", "")

    if file_type in ["txt", "md"]:
        return extract_text_from_txt_or_md(file_bytes)
    elif file_type == "pdf":
        return extract_text_from_pdf(file_bytes)
    elif file_type == "docx":
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError(f"Formato de arquivo não suportado: {file_type}")

