from importlib import import_module


FastAPI = import_module("fastapi").FastAPI


app = FastAPI(
    title="AI Interview Preparation System",
    description=(
        "Generative AI + Deep Learning/NLP based "
        "adaptive interview preparation system."
    ),
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "AI Interview Preparation System API",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }