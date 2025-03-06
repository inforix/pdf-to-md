# User Flow & Project Structure

## User Journey

### PDF Conversion Flow

1. User prepares a PDF file or URL to a PDF
2. User makes a POST request to `/convert` endpoint with the file or URL
3. System processes the PDF and converts it to markdown
4. System returns the markdown content to the user

### Image Processing Flow

1. User prepares an image file or URL to an image
2. User makes a POST request to `/convert` endpoint with the file or URL
3. System detects that the file is an image based on extension
4. System applies OCR to extract text from the image
5. System returns the extracted text as markdown to the user

### PDF with Image Extraction Flow

1. User prepares a PDF file or URL to a PDF
2. User makes a POST request to `/convert` endpoint with the file or URL and `convert_image=true`
3. System processes the PDF and converts it to markdown
4. System extracts images from the PDF and applies OCR to them
5. System includes the extracted image text in the markdown
6. System returns the enhanced markdown content to the user

## Data Flow

1. **Input Reception**
   - API receives file upload or URL
   - Validates input parameters

2. **File Type Detection**
   - Determines if input is PDF or image based on extension
   - Routes to appropriate processing pipeline

3. **Processing**
   - PDF Processing: Converts PDF to markdown
   - Image Processing: Applies OCR to extract text
   - PDF with Image: Extracts and processes embedded images

4. **Caching**
   - Generates cache key based on content and parameters
   - Checks cache for existing results
   - Stores new results in cache

5. **Response**
   - Returns processed markdown content
   - Includes any error information if processing failed

## Project File Structure

```
pdf-to-md/
├── app/                      # Main application code
│   ├── api/                  # API endpoints
│   │   ├── __init__.py
│   │   └── routes.py         # API route definitions
│   ├── core/                 # Core functionality
│   │   ├── __init__.py
│   │   └── cache.py          # Caching implementation
│   ├── services/             # Business logic
│   │   ├── __init__.py
│   │   └── pdf_service.py    # PDF and image processing service
│   └── main.py               # Application entry point
├── docs/                     # Documentation
│   ├── features.md           # Feature documentation
│   ├── overview.md           # Project overview
│   ├── requirements.md       # Requirements specification
│   ├── tech-specs.md         # Technical specifications
│   ├── user-structure.md     # User flow and structure
│   └── task.md               # Original task description
├── output/                   # Output directory for processed files
│   └── images/               # Directory for extracted images
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose configuration
├── requirements.txt          # Python dependencies
├── magic-pdf.template.json   # MinerU configuration
└── README.MD                 # Project README
```

## Component Interactions

1. **API Layer (routes.py)**
   - Receives HTTP requests
   - Validates input parameters
   - Calls appropriate service methods
   - Returns HTTP responses

2. **Service Layer (pdf_service.py)**
   - Contains business logic for processing
   - Handles file type detection
   - Manages processing pipelines
   - Interacts with caching system

3. **Core Layer (cache.py)**
   - Provides caching functionality
   - Manages cache keys and values
   - Handles cache hits and misses

4. **External Dependencies**
   - MinerU: PDF and image processing
   - Redis: Caching (optional) 