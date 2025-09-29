import asyncio
import uvicorn
from main import app

async def main():
    config = uvicorn.Config(app, host="0.0.0.0", port=5050, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
