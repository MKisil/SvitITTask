from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.logs.router import router as logs_router

app = FastAPI(title="Test task")

app.include_router(auth_router)
app.include_router(logs_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
