import uvicorn
from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("__name__")

app = FastAPI()


@app.get("/test")
async def test():
    logger.info("Received request")
    return "Hello Code Debugger!"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)