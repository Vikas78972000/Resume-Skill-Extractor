from fastapi import FastAPI
from .routes.api import router
from .middleware.logging import LoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.routes import skills 
# Load environment variables
load_dotenv()

# ✅ Define the FastAPI app
app = FastAPI(
    title=os.getenv("APP_NAME", "FastAPI Backend"),
    version=os.getenv("API_VERSION", "v1")
)

#  Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Add logging middleware
app.add_middleware(LoggingMiddleware)

#  Include API routes
app.include_router(router, prefix="/api")            # General API routes
app.include_router(skills.router, prefix="/api/v1")  # Skills route

#  Health check route
@app.get("/")
def read_root():
    return {
        "message": "Hello World from FastAPI!",
        "app_name": os.getenv("APP_NAME", "FastAPI Backend"),
        "version": os.getenv("API_VERSION", "v1")
    }
