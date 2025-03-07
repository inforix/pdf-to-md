import hashlib
import os
import tempfile
from pathlib import Path
import requests
import re
from magic_pdf.data.dataset import PymuDocDataset
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
from magic_pdf.config.enums import SupportedPdfParseMethod
from magic_pdf.data.data_reader_writer import FileBasedDataWriter
from app.core.cache import get_cache, set_cache
from magic_pdf.data.read_api import read_local_images, read_local_office

class PDFService:
    def __init__(self):
        # Create output directories
        self.output_dir = Path("output")
        self.image_dir = self.output_dir / "images"
        self.output_dir.mkdir(exist_ok=True)
        self.image_dir.mkdir(exist_ok=True)
                
        # Initialize writers
        self.image_writer = FileBasedDataWriter(str(self.image_dir))
        self.md_writer = FileBasedDataWriter(str(self.output_dir))

    @staticmethod
    def _generate_cache_key(content: bytes, convert_image: bool) -> str:
        # Combine content and convert_image flag to create unique cache key
        return hashlib.md5(content).hexdigest() + str(convert_image)

    @staticmethod
    def _download_pdf(url: str) -> bytes:
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    @staticmethod
    def _is_image_file(filename: str) -> bool:
        """Check if the filename has an image extension."""
        image_extensions = ['.jpg', '.jpeg', '.png']
        return any(filename.lower().endswith(ext) for ext in image_extensions)
    
    @staticmethod
    def _is_office_file(filename: str) -> bool:
        """Check if the filename has an office extension."""
        office_extensions = ['.docx', '.doc', '.xls', '.xlsx', '.ppt', '.pptx']
        return any(filename.lower().endswith(ext) for ext in office_extensions)
    
    def _process_image_in_markdown(self, markdown_content: str) -> str:
        """Process images in markdown content and extract text using MinerU."""
        # Regular expression to find markdown image syntax
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        
        def replace_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            
            if image_path.startswith('images/'):
                full_img_path = self.output_dir / image_path
                if full_img_path.exists():
                    # Create a new dataset for the image
                    with open(full_img_path, 'rb') as img_file:
                        img_content = img_file.read()
                    
                    try:
                        # Process image with MinerU
                        ds = read_local_images(full_img_path)[0]
                        infer_result = ds.apply(doc_analyze, ocr=True)
                        pipe_result = infer_result.pipe_ocr_mode(self.image_writer)
                        
                        # Get OCR text
                        temp_md_path = self.output_dir / f"temp_{Path(image_path).stem}.md"
                        pipe_result.dump_md(self.md_writer, temp_md_path.name, "images")
                        ocr_text = temp_md_path.read_text().strip()
                        temp_md_path.unlink()  # Clean up temporary file
                        
                        # clear image_pattern in ocr_text
                        ocr_text = re.sub(image_pattern, '', ocr_text)
                        if ocr_text:
                            # Return both the image reference and extracted text
                            return f"{match.group(0)}\n\n**Image Text:**\n{ocr_text}\n"
                    except Exception as e:
                        print(f"Error processing image {image_path}: {e}")
            
            return match.group(0)  # Return original image reference if processing fails
        
        # Replace all image references with image + extracted text
        return re.sub(image_pattern, replace_image, markdown_content)

    def process_image(self, content: bytes, filename: str) -> str:
        """Process an image file directly using OCR."""
        # Get image extension from filename
        suffix = os.path.splitext(filename)[1]
        # Create a temporary file for the image
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp_file:
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Process image with MinerU
            ds = read_local_images(tmp_path)[0]
            infer_result = ds.apply(doc_analyze, ocr=True)
            pipe_result = infer_result.pipe_ocr_mode(self.image_writer)
            
            # Generate a unique name for this conversion
            name = hashlib.md5(content).hexdigest()[:8]
            
            # Dump markdown
            pipe_result.dump_md(self.md_writer, f"{name}.md", "images")
            
            # Read the generated markdown file
            markdown_path = self.output_dir / f"{name}.md"
            markdown_content = markdown_path.read_text()
            
            return markdown_content
            
        finally:
            # Clean up temporary files
            Path(tmp_path).unlink()

    def process_pdf(self, content: bytes, filename: str, convert_image: bool = False) -> str:
        cache_key = self._generate_cache_key(content, convert_image)
        
        # Check cache first
        cached_result = get_cache(cache_key)
        if cached_result:
            return cached_result

        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(content)
            tmp_path = tmp_file.name

        try:
            # Create Dataset Instance
            ds = PymuDocDataset(content)
            
            # Determine if OCR is needed if not explicitly specified
            needs_ocr = ds.classify() == SupportedPdfParseMethod.OCR
            
            # Process the PDF
            infer_result = ds.apply(doc_analyze, ocr=needs_ocr)
            
            # Apply appropriate pipeline
            if needs_ocr:
                pipe_result = infer_result.pipe_ocr_mode(self.image_writer)
            else:
                pipe_result = infer_result.pipe_txt_mode(self.image_writer)

            # Generate a unique name for this conversion
            name = cache_key[:8]
            
            # Dump markdown
            pipe_result.dump_md(self.md_writer, f"{name}.md", "images")
            
            # Read the generated markdown file
            markdown_path = self.output_dir / f"{name}.md"
            markdown_content = markdown_path.read_text()
            
            # Process images in the markdown content
            if convert_image:
                markdown_content = self._process_image_in_markdown(markdown_content)
            
            # Cache the result
            set_cache(cache_key, markdown_content)
            
            return markdown_content
            
        finally:
            # Clean up temporary files
            Path(tmp_path).unlink()
            
    def process_office(self, content: bytes, filename: str, convert_image: bool = False) -> str:
        """Process an office file using LibreOffice."""
        
        # Get office extension from filename
        suffix = os.path.splitext(filename)[1]
        
        # Create a temporary file for the office file
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp_file:
            tmp_file.write(content)
            tmp_path = tmp_file.name

        cache_key = self._generate_cache_key(content, convert_image)
        
        # Check cache first
        cached_result = get_cache(cache_key)
        if cached_result:
            return cached_result

        # Convert office file to PDF
        try:
            # Create Dataset Instance
            ds = read_local_office(tmp_path)[0]
            
            # Determine if OCR is needed if not explicitly specified
            needs_ocr = ds.classify() == SupportedPdfParseMethod.OCR
            
            # Process the PDF
            infer_result = ds.apply(doc_analyze, ocr=needs_ocr)
            
            # Apply appropriate pipeline
            if needs_ocr:
                pipe_result = infer_result.pipe_ocr_mode(self.image_writer)
            else:
                pipe_result = infer_result.pipe_txt_mode(self.image_writer)

            # Generate a unique name for this conversion
            name = cache_key[:8]
            
            # Dump markdown
            pipe_result.dump_md(self.md_writer, f"{name}.md", "images")
            
            # Read the generated markdown file
            markdown_path = self.output_dir / f"{name}.md"
            markdown_content = markdown_path.read_text()
            
            # Process images in the markdown content
            if convert_image:
                markdown_content = self._process_image_in_markdown(markdown_content)
            
            # Cache the result
            set_cache(cache_key, markdown_content)
            
            return markdown_content
            
        finally:
            # Clean up temporary files
            Path(tmp_path).unlink()
            
    
    def process_url(self, url: str, convert_image: bool = False) -> str:
        # Get filename from URL
        filename = os.path.basename(url)
        # Check if URL points to an image
        if self._is_image_file(filename):
            content = self._download_pdf(url)  # Reusing the download method
            return self.process_image(content, filename)
        elif self._is_office_file(filename):
            content = self._download_pdf(url)
            return self.process_office(content, filename)
        else:
            content = self._download_pdf(url)
            return self.process_pdf(content, convert_image) 