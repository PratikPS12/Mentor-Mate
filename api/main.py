from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import db_manager
from app.routes import (
    auth_routes,
    student_routes,
    marksheet_routes,
    assessment_routes,
    planner_routes,
    tutor_routes,
    recommendation_routes,
    performance_routes,
    ai_routes,
    guidance_routes
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect database
    await db_manager.connect()
    print("Mentor Mate API initialized successfully.")
    yield
    # Shutdown: close connections
    await db_manager.close()
    print("Mentor Mate API shut down cleanly.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
prefix = settings.API_PREFIX
app.include_router(auth_routes.router, prefix=prefix)
app.include_router(student_routes.router, prefix=prefix)
app.include_router(marksheet_routes.router, prefix=prefix)
app.include_router(assessment_routes.router, prefix=prefix)
app.include_router(planner_routes.router, prefix=prefix)
app.include_router(tutor_routes.router, prefix=prefix)
app.include_router(recommendation_routes.router, prefix=prefix)
app.include_router(performance_routes.router, prefix=prefix)
app.include_router(ai_routes.router, prefix=prefix)
app.include_router(guidance_routes.router, prefix=prefix)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "is_atlas": db_manager.is_atlas
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

