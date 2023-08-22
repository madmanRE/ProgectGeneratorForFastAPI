from fastapi import FastAPI, Request, HTTPException, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from routers import auth_router, book_router


from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from sqladmin import Admin, ModelView
from database import engine, User
from models import *

from starlette.responses import RedirectResponse

app = FastAPI(title="ProjectGenerator")
admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.email,
        User.is_active,
        User.is_superuser,
    ]
    column_details_exclude_list = [User.hashed_password]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


admin.add_view(UserAdmin)

app.include_router(auth_router.auth_router)
app.include_router(book_router.book_router)


class RedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if str(request.url)[:-1].split("/")[-1] == "admin":
            return RedirectResponse(url="/protected-admin")
        response = await call_next(request)
        return response


app.add_middleware(RedirectMiddleware)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(
        "redis://localhost:6379", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
