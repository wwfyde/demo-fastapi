from fastapi import APIRouter
from starlette.requests import Request

router = APIRouter()


@router.get("/app_state", summary="Get application state")
async def get_app_state(request: Request):
    state = request.app.state
    state.request_count += 1
    return {"request_count": state.request_count}
