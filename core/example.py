from fastapi import HTTPException
# from db.mssql import MSSQLBase
from db.mssql import MSSQLBaseSingleton as MSSQLBase
from pydantic import BaseModel
import pandas as pd

# TODO:
# class User(BaseModel):
#     name: str
#     age: int

class MyReesponse(BaseModel):
    status_code: int
    message: dict

def get_users() -> MyReesponse:
    db = MSSQLBase()
    print(F'DB info: {id(db)}')
    sql = 'select * from backend_users'
    results = db.query(sql)
    if len(results) == 0:
        return MyReesponse(status_code=204, message={'detail': 'No accounts','data': {}})
    return MyReesponse(status_code=200, message={'data': [{'name': name, 'age': age} for name, age in results]})

def get_group_avg_age() -> MyReesponse:
    db = MSSQLBase()
    print(F'DB info: {id(db)}')
    sql = 'select * from backend_users'
    results = db.query(sql)

    if len(results) == 0:
        return MyReesponse(status_code=204, message={'detail': 'No accounts','data': {}})
    
    df = pd.DataFrame(results, columns=['Name', 'Age'])
    df_avg_result = df.groupby(df['Name'].str[0]).agg(avg_age=('Age', 'mean'))
    df_avg_result = df_avg_result.reset_index(drop=False)
    df_avg_result = df_avg_result.rename(columns={'Name': 'group'})

    return MyReesponse(status_code=200, message={'data': df_avg_result.to_dict(orient="records")})
    
def add_user(name:str, age:int, table:str="backend_users") -> MyReesponse:
    db = MSSQLBase()
    print(F'DB info: {id(db)}')
    sql = f"select * from {table} where name='{name}'"
    results = db.query(sql)
    if len(results) > 0:
        raise HTTPException(status_code=400, detail={'message': f'{name} is already in db'})

    try:
        columns = ['Name', 'Age']
        values = (name, age)
        db.insert(table, columns, values)
        return MyReesponse(status_code=200, message={'message': f'insert {name} to db'})
    except Exception as e:
        raise HTTPException(status_code=400, detail={'message': f'error: {e}'})

def add_users(file) -> MyReesponse:
    df = pd.read_csv(file.file)
    db = MSSQLBase()
    print(F'DB info: {id(db)}')
    db.insert_by_df(df, table="backend_users")
    return MyReesponse(status_code=200, message={'message': f'add csv to db'})
    
def delete_user(name:str, table:str="backend_users") -> MyReesponse:
    db = MSSQLBase()
    print(F'DB info: {id(db)}')
    condition = f"Name='{name}'"
    sql = f"select * from {table} where {condition}"
    results = db.query(sql)
    if len(results) > 0:
        db.delete(table, condition)
        return MyReesponse(status_code=200, message={'message': f'delete {name} from db'})
    else:
        raise HTTPException(status_code=400, detail={'message': f'{name} not in db'})
    

    





