# test_simple.py
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/test")
def test():
    return {"message": "Python and FastAPI are working!"}

if __name__ == "__main__":
    print("Testing basic server...")
    uvicorn.run(app, host="0.0.0.0", port=5002)
