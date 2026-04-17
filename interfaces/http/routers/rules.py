from fastapi import APIRouter


router = APIRouter()


@router.get("")
def list_rules() -> dict[str, list]:
    return {"items": []}
