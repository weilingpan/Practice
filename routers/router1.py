from fastapi import APIRouter, File, UploadFile, HTTPException
from core import example

router = APIRouter(tags=['HW API'], prefix="/hw")

@router.get("/get_users/")
async def get_users():
    return example.get_users()

@router.get("/get_group_avg_age/")
async def get_group_avg_age():
    return example.get_group_avg_age()

@router.post("/add_user/")
async def add_user(name:str, age:str):
    return example.add_user(name, age)

@router.post("/add_users/")
async def add_users(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    return example.add_users(file)

@router.delete("/del_user/{name}")
async def delete_user(name:str):
    return example.delete_user(name)

