from fastapi import FastAPI
from database import Base, engine
from routers.api import router as api_router
from routers.debug import router as debug_router
from fastapi.middleware.cors import CORSMiddleware   
# create tables
Base.metadata.create_all(bind=engine)



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              
    allow_credentials=True,
    allow_methods=["*"],              
    allow_headers=["*"],
)

app.include_router(api_router)

app.include_router(debug_router)

@app.get("/")
def read_root():    
    return {"message": "Welcome to the File Upload API"}
