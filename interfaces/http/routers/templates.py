from fastapi import APIRouter


router = APIRouter()


@router.get("")
def list_templates() -> dict[str, list]:
    return {"items": []}
