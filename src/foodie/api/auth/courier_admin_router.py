from fastapi import APIRouter


router = APIRouter()


@router.post("/auth", response_model=None)
def authenticate():
    pass
