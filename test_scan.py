from fastapi import FastAPI
import uvicorn

app = FastAPI()

# Minimal test endpoint
@app.get("/api/test/scan")
async def test_scan():
    return {
        "status": "success",
        "message": "Test endpoint is working",
        "results": [
            {"host": "test.local", "status": "up"}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
