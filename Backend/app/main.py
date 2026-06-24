import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib

from app.core.config import settings
from app.api.routers import router as api_router
from app.api.auth import auth_router  
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Log initialization parameters 
    print("[Server Init Block] Executing structural loading profiles across ML Artifact stores.")
    
    if not os.path.exists(settings.PRICING_MODEL_PATH) or not os.path.exists(settings.CHURN_MODEL_PATH):
        raise FileNotFoundError(
            "Artifact binaries missing from compilation targets. "
            "Please explicitly run compilation tools in backend/src/ beforehand."
        )
        
    app.state.pricing_pipeline = joblib.load(settings.PRICING_MODEL_PATH)
    app.state.churn_pipeline = joblib.load(settings.CHURN_MODEL_PATH)
    
    print("[Initialization Complete] Framework matrices mapped directly inside operational memory space.")
    yield
    print("[Teardown Sequence Initiated] Cleaning down tracking nodes.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["System Diagnostics"])
async def get_health_status():
    return {"status": "operational", "engine_state": "synchronized"}

app = FastAPI(title="Shield Core Matrix Engine", version="1.2")

# Initialize database tables on server start
@app.on_event("startup")
def on_startup():
    init_db()  # <-- 3. Creates the database tables automatically

# Configure CORS so your React frontend can talk to the backend safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your Vite frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(api_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")