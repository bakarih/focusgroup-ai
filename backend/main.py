from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import simulations, websocket

app = FastAPI(title="FocusGroup.AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulations.router)
app.include_router(websocket.router)
