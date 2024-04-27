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
