from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, rag
from app.routes.upload import router as upload_router  # Correct import
from app.db.database import Base, engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # (Optional) Cleanup code can go here

app = FastAPI(lifespan=lifespan)

# ✅ Enable CORS (Make sure to restrict origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include your routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(rag.router, prefix="/chat", tags=["Chat"])
app.include_router(upload_router, prefix="/upload", tags=["Upload"])  # Include upload router
