from fastapi import APIRouter

router = APIRouter()

@router.get("/taxonomy")
def get_taxonomy():
    return {"message": "taxonomy endpoint (to implement)"} 