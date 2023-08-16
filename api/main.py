
import os
from typer import Typer
from cryptography.fernet import Fernet
import encryption

app = Typer()

@app.command()
def encrypt(path: str, compLvl: int = 9, file: bool = False):
    password = Fernet.generate_key()
    outPath = path + ".enc"
    if file:
        if not os.path.exists(path) or not os.path.isfile(path):
            print("Not a valid file path")
        
        encryption.encryptFile(path, password, outPath)
        # encryption.compressFile(outPath, outPath, compLvl)
    else:
        if not os.path.exists(path) or os.path.isfile(path):
            print("Not a valid folder path")
        
        encryption.encryptFolder(path, password, outPath)
        # encryption.compressFolder(outPath, outPath, compLvl)
        print(f"Encrypting folder {path} to {outPath} with compression level {compLvl}")

    print(password.decode())

@app.command()
def decrypt(path: str, key: str, file: bool = False):
    outPath = path.replace(".enc", "_")
    key = bytes(key, 'utf-8')
    if file:
        print(f"Decrypting file {path} to {outPath} with key {key}")
    else:
        encryption.decryptFolder(path, key, outPath)

if __name__ == "__main__":
    app()