from fastapi import FastAPI
from src.api import document_ingestion, user, document_selection, qa
from src.database import Base, engine
from src.utils.logging_utils import LoggingUtils

# Initialize logger
logger = LoggingUtils.get_logger(__name__)

# Create FastAPI app
app = FastAPI()

# Create database tables
logger.info("Creating database tables")
Base.metadata.create_all(bind=engine)

# Include routers
logger.info("Including API routers")
app.include_router(document_ingestion.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(document_selection.router, prefix="/api/v1")
app.include_router(qa.router, prefix="/api/v1")

# Application startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")

# Application shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
