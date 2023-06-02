import uvicorn
from fastapi import FastAPI

from cremusic.api import api_router, index_router

app = FastAPI()
app.include_router(index_router)
app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("app:app", port=8000, host='127.0.0.1')
