import uvicorn
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from routers import demo, user
import utils

settings = utils.get_settings()
api_title = settings.api_name
api_description = settings.api_description
app = FastAPI(title=api_title, description=api_description)

app.include_router(
    demo.router,
    prefix="/demo",
    tags=["demo"],
)

app.include_router(
    user.router,
    prefix="/user",
    tags=["user"],
)


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host='0.0.0.0')

# conda activate pegatron
# uvicorn main:app --reload