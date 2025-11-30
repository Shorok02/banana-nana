from fastapi import FastAPI
from database import Base, engine
from routers.files import router as file_router
from routers.debug import router as debug_router
from routers.ask import router as ask_router 
from fastapi.middleware.cors import CORSMiddleware   
# create tables
Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],               # change later to your domain for security
    allow_credentials=True,
    allow_methods=["*"],               #  <--- this allows POST + OPTIONS
    allow_headers=["*"],
)

app.include_router(file_router)

app.include_router(debug_router)
app.include_router(ask_router)

@app.get("/")
def read_root():    
    return {"message": "Welcome to the File Upload API"}
