from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
from app.services.pdf_service import PDFService

router = APIRouter()
pdf_service = PDFService()

@router.post("/convert/")
async def convert_pdf(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = None,
    needs_ocr: bool = True,
):
    try:
        print(f"needs_ocr: {needs_ocr}")
        if file:
            content = await file.read()
            return {"markdown": pdf_service.process_pdf(content, needs_ocr)}
        elif url:
            return {"markdown": pdf_service.process_pdf_url(url, needs_ocr)}
        else:
            raise HTTPException(
                status_code=400,
                detail="Either file or url must be provided"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 