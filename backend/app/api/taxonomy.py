from fastapi import APIRouter

router = APIRouter()

@router.get("/taxonomy")
async def get_taxonomy():
    return {"message": "Hello, world!"}