from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.routes import driver
from app.routes import truck

# Import models so SQLAlchemy knows about the tables
from app.models import driver as driver_model
from app.models import truck as truck_model


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Dispatch OS API",
    version="1.0.0"
)


# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
app.include_router(driver.router)
app.include_router(truck.router)


@app.get("/")
def read_root():
    return {
        "message": "Dispatch OS API running"
    }
