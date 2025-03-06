from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
from app.services.pdf_service import PDFService

router = APIRouter()
pdf_service = PDFService()

@router.post("/convert")
async def convert_pdf(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    convert_image: bool = Form(False),
):
    try:
        print(f"convert_image: {convert_image}")
        if file:
            content = await file.read()
            # Check if the uploaded file is an image
            if pdf_service._is_image_file(file.filename):
                return {"markdown": pdf_service.process_image(content)}
            else:
                return {"markdown": pdf_service.process_pdf(content, convert_image)}
        elif url:
            return {"markdown": pdf_service.process_pdf_url(url, convert_image)}
        else:
            raise HTTPException(
                status_code=400,
                detail="Either file or url must be provided"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 