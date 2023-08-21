from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from auth.auth_config import auth_backend
from database import User
from auth.manager import get_user_manager
from schemas.schemas import UserRead, UserCreate
from starlette.responses import RedirectResponse

auth_router = APIRouter()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@auth_router.get("/protected-admin")
def get_admin(user: User = Depends(current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Forbidden")
    return RedirectResponse(url="/admin/?enter=true/")
