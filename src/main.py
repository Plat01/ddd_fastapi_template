from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.infrastructure.database import init_db
from src.presentation.routers import api_router
from src.config import get_settings

@asynccontextmanager  
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Auth API",
    lifespan=lifespan
)

app.add_middleware(
    SessionMiddleware,
    secret_key=get_settings().SECRET_KEY,
    # http_only=True, # TODO: set to True in production
    # store=RedisSession(redis)  # TODO: ass Reddis storage
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TOOD:  set to specific origin from settings
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=get_settings().API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Hello World"}
