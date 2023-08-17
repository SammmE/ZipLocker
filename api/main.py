import uvicorn

from cryptography.fernet import Fernet
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import encryption

from pydantic import BaseModel

class encrypt(BaseModel):
    folderPath: str
    outFolderPath: str

class decrypt(BaseModel):
    folderPath: str
    password: str
    outFolderPath: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post("/encrypt")
def encrypt(request: encrypt):
    password = Fernet.generate_key()
    encryption.encryptFolder(request.folderPath, password, request.outFolderPath)
    return {"status": "success", "password": password}

@app.post("/decrypt")
def decrypt(request: decrypt):
    encryption.decryptFolder(request.folderPath, request.password, request.outFolderPath)
    return {"status": "success"}

def serve():
    uvicorn.run(app, host="localhost", port=8000)

if __name__ == "__main__":
    serve()