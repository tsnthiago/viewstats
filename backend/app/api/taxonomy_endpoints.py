from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
import os, json
from app.services import taxonomy_service

router = APIRouter()

API_KEY = os.environ.get("INTERNAL_API_KEY", "SUA_CHAVE_SECRETA_AQUI")

def verify_api_key(request: Request):
    key = request.headers.get("X-Internal-API-Key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

@router.get("/taxonomy")
def get_taxonomy():
    return taxonomy_service.get_taxonomy()

@router.post("/taxonomy/upload")
def upload_taxonomy(
    taxonomy_file: UploadFile = File(...),
    _: None = Depends(verify_api_key)
):
    try:
        content = taxonomy_file.file.read()
        data = json.loads(content)
        taxonomy_service.update_taxonomy(data)
        return {"message": "Taxonomy updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid taxonomy file: {e}") 