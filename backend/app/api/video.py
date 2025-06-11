from fastapi import APIRouter

router = APIRouter()

@router.get("/video/{id}")
def get_video(id: str):
    return {"message": f"video endpoint for id {id} (to implement)"} 