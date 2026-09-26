from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

# Models must be imported before create_all so SQLAlchemy
# knows about every table.
from app.models import driver as driver_model
from app.models import truck as truck_model
from app.models import load as load_model
from app.models import expense as expense_model

from app.routes import driver
from app.routes import truck
from app.routes import load
from app.routes import expense


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Dispatch OS API",
    version="1.0.0",
    description="Left Door Shut Dispatch management platform API",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(driver.router)
app.include_router(truck.router)
app.include_router(load.router)
app.include_router(expense.router)


@app.get("/")
def read_root():
    return {
        "message": "Dispatch OS API running",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "dispatch-os-api",
        "version": "1.0.0",
    }
