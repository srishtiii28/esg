import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF for PDF processing

class OCRProcessor:
    def __init__(self):
        self.supported_formats = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff'}

    async def extract_text(self, file_content: bytes, filename: str) -> str:
        """Extract text from document using OCR if needed"""
        try:
            ext = '.' + filename.split('.')[-1].lower()
            
            if ext not in self.supported_formats:
                raise ValueError(f"Unsupported file format: {ext}. Supported formats: {', '.join(self.supported_formats)}")

            if ext == '.pdf':
                return await self._process_pdf(file_content)
            else:
                return await self._process_image(file_content)
        except Exception as e:
            raise ValueError(f"Error processing file {filename}: {str(e)}")

    async def _process_pdf(self, content: bytes) -> str:
        """Extract text from PDF, using OCR if needed"""
        try:
            text = []
            pdf_doc = fitz.open(stream=content, filetype="pdf")
            
            for page_num in range(len(pdf_doc)):
                try:
                    page = pdf_doc[page_num]
                    # Try to extract text directly first
                    page_text = page.get_text()
                    
                    # If no text found, try OCR
                    if not page_text.strip():
                        pix = page.get_pixmap()
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        page_text = pytesseract.image_to_string(img)
                    
                    text.append(page_text)
                except Exception as e:
                    print(f"Warning: Error processing page {page_num}: {str(e)}")
                    text.append(f"[Error processing page {page_num}]")
            
            if not text:
                raise ValueError("No text could be extracted from the PDF")
                
            return "\n".join(text)
        except Exception as e:
            raise ValueError(f"Error processing PDF: {str(e)}")

    async def _process_image(self, content: bytes) -> str:
        """Process image files using OCR"""
        try:
            image = Image.open(io.BytesIO(content))
            text = pytesseract.image_to_string(image)
            if not text.strip():
                raise ValueError("No text could be extracted from the image")
            return text
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")
