# Instructions to Cursor

## Project Overview

This project is a FastAPI-based service that converts PDF documents and images to markdown format. It uses OCR technology to extract text from scanned documents and images.

## Key Features

1. **PDF to Markdown Conversion**: Convert PDF files to markdown format
2. **Image Processing**: Extract text from images using OCR
3. **URL-based Processing**: Process files from URLs
4. **Embedded Image Processing**: Extract and process images in PDFs

## Development Guidelines

When working on this project in Cursor, please follow these guidelines:

1. **Code Organization**
   - Keep the existing project structure
   - Place new features in appropriate modules
   - Follow the established patterns for API routes and services

2. **Error Handling**
   - Use try-except blocks for error handling
   - Return appropriate HTTP status codes
   - Provide detailed error messages

3. **Documentation**
   - Update documentation when adding new features
   - Add docstrings to new functions and classes
   - Keep the README and feature documentation up to date

4. **Testing**
   - Test new features with various input types
   - Verify error handling works as expected
   - Check performance with large files

## Common Tasks

### Adding a New Feature

1. Update the appropriate service in `app/services/`
2. Add or modify API routes in `app/api/routes.py`
3. Update documentation in `docs/`
4. Test the feature with various inputs

### Fixing a Bug

1. Identify the source of the bug
2. Add appropriate error handling
3. Fix the underlying issue
4. Test to ensure the bug is resolved
5. Update documentation if necessary

### Improving Performance

1. Identify performance bottlenecks
2. Optimize processing algorithms
3. Enhance caching mechanisms
4. Test performance improvements

## Contact

For questions or issues, please contact the project maintainer. 