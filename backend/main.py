from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dependencies.database import get_db
from routers import api_router
from services.init_db import init_roles


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- STARTUP actions ----
    db = next(get_db())
    init_roles(db)

    yield


app = FastAPI(lifespan=lifespan)

# Register routers
app.include_router(api_router, prefix="/api")

# CORS settings
origins = [
    "http://localhost:5173",  # Vue 3 default dev server (Vite)
    "http://127.0.0.1:5173",
    "https://frontend-dot-lyrical-oath-458519-k1.oa.r.appspot.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def app_settings():
    return {
        "message": "Welcome to RESERWEB backend!",
        "docs": "https://lyrical-oath-458519-k1.oa.r.appspot.com/docs",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
