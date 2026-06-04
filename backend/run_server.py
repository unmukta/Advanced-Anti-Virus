# backend/run_server.py
import asyncio
import uvicorn
import sys
import os

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def main():
    config = uvicorn.Config("main:app", host="0.0.0.0", port=5050, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
