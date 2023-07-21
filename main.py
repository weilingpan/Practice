import uvicorn
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from routers import router1
import utils

settings = utils.get_settings()
api_title = settings.api_name
api_description = settings.api_description
app = FastAPI(title=api_title, description=api_description)
app.include_router(router1.router)

@app.get("/")
def welcome():
    return {"welcome": "Hello World"}

@app.get("/demo/")
async def read_users():
    return [{"username": "Amy", "userage": 34}, {"username": "John", "userage": 67}]

@app.get("/demo/hello")
async def hello_user(user: str="Regina"):
    return {"Hello": user}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host='0.0.0.0')

# conda activate pegatron
# uvicorn main:app --reload