from fastapi import FastAPI, Depends
from schemas.student import Student
from config.db import conn,SessionLocal
from models.index import students
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Dict, Any
app=FastAPI()

# best way to make api
# @app.get('/api/students',response_model=list[Student])
# async def index():
#     data=conn.execute(students.select()).fetchall()
#     # conn.commit()
#     return {
#         "success": True,
#         "data":data
#     }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get('/api/students', response_model=dict)
# async def index(db: Session = Depends(get_db)):
#     query = select(students)
#     result = db.execute(query).fetchall()
#      data = [{"name": row.name, "age": row.age, "country": row.country} for row in result]
#     return {
#         "success": True,
#         "data": data
#     }

@app.get('/api/students', response_model=Dict[str, Any])
async def index(db: Session = Depends(get_db)):
    query = select(students)
    result = db.execute(query).fetchall()
    
    # Mengkonversi hasil query menjadi format yang dapat di-serialize oleh Pydantic
    data = [{"name": row.name, "age": row.age, "country": row.country} for row in result]
    
    return {
        "success": True,
        "data": data
    }

# insert data
@app.post('/api/students')
async def store(student:Student):
    data=conn.execute(students.insert().values(
        name=student.name,
        age=student.age,
        country=student.country,
    ))
    conn.commit()
    if data.is_insert:
        return {
            "success": True,
            "msg":"Student Store Successfully"
        }
    else:
         return {
            "success": False,
            "msg":"Some Problem"
        }

# # edit data
# @app.patch('/api/students/{id}')
# async def edit_data(id:int):
#     data=conn.execute(students.select().where(students.c.id==id)).fetchall()
#     return {
#         "success": True,
#         "data":data
#     }

# update data

@app.put('/api/students/{id}')
async def update(id:int,student:Student):
    data=conn.execute(students.update().values(
        name=student.name,
        age=student.age,
        country=student.country,
    ).where(students.c.id==id))
    conn.commit()
    if data:
        return {
            "success": True,
            "msg":"Student Update Successfully"
        }
    else:
         return {
            "success": False,
            "msg":"Some Problem"
        }

# delete data
@app.delete('/api/students/{id}')
async def delete(id:int):
    data=conn.execute(students.delete().where(students.c.id==id))
    conn.commit()
    if data:
        return {
            "success": True,
            "msg":"Student Delete Successfully"
        }
    else:
         return {
            "success": False,
            "msg":"Some Problem"
        }

# search data

@app.get('/api/students-nama/{search}',response_model=Dict[str, Any])
async def search(nama: str, db: Session = Depends(get_db)):
    # data= conn.execute(students.select().where(students.c.name.like('%'+search+'%'))).fetchall()
    result = db.execute(select(students).where(students.c.name.like('%' + nama + '%'))).fetchall()
    data = [{"name": row.name, "age": row.age, "country": row.country} for row in result]

    # conn.commit()
    return {
        "success": True,
        "data":data
    }

@app.get('/api/students-id/{search}',response_model=Dict[str, Any])
async def search(id: str, db: Session = Depends(get_db)):
    # data= conn.execute(students.select().where(students.c.name.like('%'+search+'%'))).fetchall()
    result = db.execute(select(students).where(students.c.id.like('%' + id + '%'))).fetchone()
    data = [{"name": result.name, "age": result.age, "country": result.country}]

    # conn.commit()
    return {
        "success": True,
        "data":data
    }    