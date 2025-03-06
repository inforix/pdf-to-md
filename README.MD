# PDF to Markdown service

This project is to build a FastAPI server to handle request for converting PDF to markdown content and processing images with OCR.

## Features

- Convert PDF files to markdown
- Process images (JPG, PNG, etc.) with OCR to extract text
- Automatically detect file types based on extensions
- Support for both file uploads and URL-based processing
- Option to extract and process images embedded in PDFs

For detailed feature documentation, see [Features Documentation](docs/features.md).

## Installation

```shell
pip install -r requirements.txt
```

### Note

If you want to use GPU, please modify `device-mode` to `gpu` in `magic-pdf.template.json`:

```json
"device-mode":"cuda",
```

## Build image

If you need proxy, then specify the `--build-arg`, or just ignore it.

```shell
sudo docker compose build --build-arg HTTPS_PROXY=http://xxxx
# DO NOT FORGET ADD http:// to your proxy string
```
