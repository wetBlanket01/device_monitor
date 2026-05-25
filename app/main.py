from contextlib import asynccontextmanager
from typing import AsyncGenerator

from loguru import logger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.devices.router import router as device_router
from app.measurements.router import router as measurement_router
from app.users.router import router as user_router
from app.tasks.router import router as task_router
from app.core.redis import init_redis


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    logger.info("Initializing FastAPI App...")
    await init_redis()
    yield
    logger.info("Stopping FastAPI App...")


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    register_routers(app)
    return app


def register_routers(app: FastAPI) -> None:
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app.include_router(device_router, prefix="/devices", tags=["Devices"])
    app.include_router(measurement_router, prefix="/devices", tags=["Measurements"])
    app.include_router(user_router, prefix="/users", tags=["Users"])
    app.include_router(task_router, prefix="/tasks", tags=["Tasks"])


app = create_app()
