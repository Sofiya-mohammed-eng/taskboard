from fastapi import FastAPI

app = FastAPI(title="Taskboard API")


@app.get("/health")
def health():
    return {"status": "ok"}
