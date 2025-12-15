from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# I allow cross-origin requests from all domains (iOS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}
