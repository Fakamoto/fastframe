from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="projectname")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from .endpoints import main

app.include_router(main.router)

