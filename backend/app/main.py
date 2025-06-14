from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from app.services.file_processor import process_csv_file
from app.api import search, video, channel
from app.api import taxonomy_endpoints
from app.services import taxonomy_service
from app.services.qdrant_service import QdrantService
import os

app = FastAPI()

qdrant_service = QdrantService(
    host=os.environ.get("QDRANT_HOST", "qdrant"),
    port=int(os.environ.get("QDRANT_PORT", 6333)),
    collection_name=os.environ.get("QDRANT_COLLECTION_NAME", "videos_viewstats")
)

app.include_router(search.router)
app.include_router(video.router)
app.include_router(channel.router)
app.include_router(taxonomy_endpoints.router)

@app.on_event("startup")
def startup_event():
    taxonomy_service.load_taxonomy()

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

@app.post("/qdrant/insert")
async def qdrant_insert(request: Request):
    data = await request.json()
    id = data["id"]
    vector = data["vector"]
    payload = data.get("payload")
    result = qdrant_service.insert_vector(id, vector, payload)
    return result