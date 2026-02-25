from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="Dispatch OS Backend",
    description="Backend API for Driver/Dispatch Platform",
    version="0.1.0"
)

# Optional: Enable CORS if frontend will connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific frontend URLs in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple root endpoint to test the server
@app.get("/")
def read_root():
    return {"message": "Dispatch OS backend is running!"}
