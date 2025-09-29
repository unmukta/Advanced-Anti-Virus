# guaranteed_server.py
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "perfect", "version": "3.0.0"}

@app.get("/test")
def test_endpoint():
    return {"message": "100% working - no errors"}

if __name__ == "__main__":
    print("✅ SERVER STARTING ON PORT 5001...")
    print("📍 http://localhost:5001")
    print("📋 Endpoints: /health, /test")
    print("📊 Docs: http://localhost:5001/docs")
    uvicorn.run(app, host="0.0.0.0", port=5001, reload=False)
