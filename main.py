import uvicorn

from fastapi import FastAPI, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from schema_and_db_connection.table_schema.database_schema import User
from schema_and_db_connection.Request.student_request import UserRequest
from schema_and_db_connection.db_connection.database_connection import SessionLocal, engine, Base

# create db connection
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/user_data", status_code=status.HTTP_201_CREATED)
def input_user_data(request: UserRequest, db: Session = Depends(get_db)):
    user_data = User(name=request.name, email=request.email, description=request.description)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {"data": request}


@app.get("/user_data/all", status_code=status.HTTP_200_OK)
async def all_user_info(db: Session = Depends(get_db)):
    all_users_info = db.query(User).all()
    if not all_users_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data list is empty")
    return {"data": all_users_info}


@app.get("/user_data/{id}", status_code=status.HTTP_200_OK)
def specific_user_info(id, db: Session = Depends(get_db)):
    user_info = db.query(User).filter(User.id == id).first()
    if user_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="info not found")
    elif not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user info list is empty")
    return {"data": user_info}


@app.delete("/user_data/all", status_code=status.HTTP_200_OK)
def delete_all_info(db: Session = Depends(get_db)):
    delete_all = db.query(User)
    delete_data = []
    if not delete_all:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no data present")
    else:
        for deletion in delete_all:
            delete_data.append(deletion)
            db.delete(deletion)
        db.commit()
    return {"message": "Deletion successful", "data": delete_data}


@app.delete("/user_data/{id}", status_code=status.HTTP_200_OK)
def delete_specific_user_info(id, db: Session = Depends(get_db)):
    delete_info = db.query(User).filter(User.id == id).delete(synchronize_session=False)

    if delete_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id is not present")

    elif not delete_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="list is empty")
    else:
        db.commit()
    return {"message": "deletion successful", "data": delete_info}





