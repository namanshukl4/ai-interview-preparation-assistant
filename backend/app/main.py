from fastapi import FastAPI

from app.api.routes.interview import router as interview_router


app = FastAPI(
    title="AI Interview Preparation System",
    description=(
        "Generative AI + Deep Learning/NLP based "
        "adaptive interview preparation system."
    ),
    version="0.1.0",
)


app.include_router(interview_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "AI Interview Preparation System API",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}