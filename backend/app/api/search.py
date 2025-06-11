from fastapi import APIRouter

router = APIRouter()

@router.post("/search")
def search():
    return {"message": "search endpoint (to implement)"} 