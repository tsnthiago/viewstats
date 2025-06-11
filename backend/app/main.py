from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from app.services.file_processor import process_csv_file

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        return JSONResponse(
            status_code=400, 
            content={"error": "File must be a CSV"}
        )
    try:
        content = await file.read()
        result = process_csv_file(content)
        return {
            "message": "CSV uploaded successfully",
            "filename": file.filename,
            **result
        }
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )