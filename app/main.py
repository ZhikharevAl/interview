from fastapi import FastAPI

app = FastAPI(title="Interview Prep App")


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a greeting message."""
    return {"message": "Hello World!"}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the health status of the application."""
    return {"status": "ok"}
