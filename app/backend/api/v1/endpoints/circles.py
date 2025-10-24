from fastapi import APIRouter

router = APIRouter()


@router.get("", response_model=list[dict])
async def get_circles():
    return []


@router.post("", response_model=dict, status_code=201)
async def create_circle():
    return {"message": "Not implemented"}


@router.get("/{circle_id}", response_model=dict)
async def get_circle_details(circle_id: str):
    return {"message": "Not implemented"}


@router.post("/{circle_id}/members", response_model=dict)
async def add_circle_member(circle_id: str):
    return {"message": "Not implemented"}