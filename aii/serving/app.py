from fastapi import FastAPI

app = FastAPI(title="NUVIE AI Service")

@app.get("/health")
def health():
    return {"status": "ai-ok"}

@app.post("/recommend")
def recommend():
    return {
        "items": [
            {"movie_id": 1, "score": 0.95, "reason": ["genre_match"]},
            {"movie_id": 2, "score": 0.90, "reason": ["friend_like"]}
        ]
    }

