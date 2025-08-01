from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import uuid
from markitdown import MarkItDown
import os
import shutil
import tempfile

app = FastAPI()
md = MarkItDown(enable_plugins=True)


@app.post("/pdf_to_markdown")
async def pdf_conversion(pdf_file: UploadFile = File(...)):
    # Create a temporary file
    suffix = os.path.splitext(pdf_file.filename)[
        1
    ]  # keep the original pdf_file extension
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        pdf_path = tmp.name
        # Save the uploaded pdf_file to the temp location
        pdf_dir = os.path.join("te" "mp", str(uuid.uuid4()))
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_path = os.path.join(pdf_dir, pdf_path)
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(pdf_file.file, buffer)

    try:
        # Now pass the file path to markitdown
        result = md.convert(pdf_path)

        return JSONResponse(
            content={
                "filename": pdf_file.filename,
                "content_type": pdf_file.content_type,
                "content": result.text_content,
            }
        )
    finally:
        # Optional: delete the temp file
        if os.path.exists(pdf_dir):
            shutil.rmtree(pdf_dir)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
