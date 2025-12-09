from fastapi import FastAPI

app = FastAPI(title="NUVIE Backend API")

@app.get("/health")
def health():
    return {"status": "ok"}
