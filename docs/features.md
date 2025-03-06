# PDF to Markdown Service Features

## Core Features

1. **PDF to Markdown Conversion**
   - Upload PDF files and convert them to markdown format
   - Provide a URL to a PDF file for conversion
   - Automatic OCR detection and processing for scanned PDFs

2. **Image Processing**
   - Direct processing of image files (JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP)
   - Automatic detection of image files based on file extension
   - OCR processing to extract text from images
   - Images can be uploaded directly or via URL

3. **Image Extraction from PDFs**
   - Option to extract and process images embedded in PDFs
   - Enable with the `convert_image` parameter

## API Endpoints

### POST /convert

Converts a PDF or image file to markdown.

**Parameters:**
- `file`: (Optional) The PDF or image file to convert
- `url`: (Optional) URL to a PDF or image file
- `convert_image`: (Optional, default: false) Whether to extract and process images in PDFs

**Response:**
```json
{
  "markdown": "# Converted content in markdown format..."
}
```

**Error Responses:**
- 400: Either file or URL must be provided
- 500: Internal server error

## Supported File Types

- PDF files (.pdf)
- Image files:
  - JPEG (.jpg, .jpeg)
  - PNG (.png)
  - GIF (.gif)
  - BMP (.bmp)
  - TIFF (.tiff)
  - WebP (.webp) 