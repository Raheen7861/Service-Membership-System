from fastapi import FastAPI

from .database import Base, engine
from .routers import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Service Membership API",
        version="1.0.0",
    )


    @app.on_event("startup")
    def on_startup():
        Base.metadata.create_all(bind=engine)

    app.include_router(api_router)
    return app


app = create_app()
