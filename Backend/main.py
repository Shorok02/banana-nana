from fastapi import FastAPI
from database import Base, engine
from routers.files import router as file_router
# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(file_router)

@app.get("/")
def read_root():    
    return {"message": "Welcome to the File Upload API"}
