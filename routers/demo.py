from fastapi import APIRouter, File, UploadFile, HTTPException

router = APIRouter()

@router.get("/")
def welcome():
    return {"welcome": "Hello World"}

@router.get("/demo/")
async def read_users():
    return [{"username": "Amy", "userage": 34}, {"username": "John", "userage": 67}]

@router.get("/demo/hello")
async def hello_user(user: str="Regina"):
    return {"Hello": user}