import os
import zipfile
import pyuac
from cryptography.fernet import Fernet

def compressFolder(folder_path, zip_file_name, compLvl=9):
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=compLvl) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

def decompressFolder(zip_file_name, extract_folder):
    with zipfile.ZipFile(zip_file_name, 'r') as zipf:
        zipf.extractall(extract_folder)

def encryptFile(filePath, key, outFilePath=None):
    if outFilePath is None:
        outFilePath = filePath
    with open(filePath, 'rb') as file:
        data = file.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    
    if os.path.exists(outFilePath):
        os.remove(outFilePath)
    open(outFilePath, 'x')
    
    open(outFilePath, 'wb').write(encrypted)

def decryptFile(filePath, key, outFilePath=None):
    if outFilePath is None:
        outFilePath = filePath
    with open(filePath, 'rb') as file:
        data = file.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    if os.path.exists(outFilePath):
        os.remove(outFilePath)
    open(outFilePath, 'x')
    
    open(outFilePath, 'wb').write(decrypted)

def encryptFolder(folderPath, key, outFolderPath=None):
    if outFolderPath is None:
        outFolderPath = folderPath
    for root, dirs, files in os.walk(folderPath):
        for file in files:
            filePath = os.path.join(root, file)

            if os.path.exists(outFolderPath):
                print("Detected existing folder. Deleting...")
                os.remove(outFolderPath)
            os.mkdir(outFolderPath)

            encryptFile(filePath, key, outFilePath=os.path.join(outFolderPath, file))

def decryptFolder(folderPath, key, outFolderPath):
    try:
        if outFolderPath is None:
            outFolderPath = folderPath
        for root, dirs, files in os.walk(folderPath):
            for file in files:
                filePath = os.path.join(root, file)

                if os.path.exists(outFolderPath):
                    print("Detected existing folder. Deleting...")
                    os.remove(outFolderPath)
                os.mkdir(outFolderPath)

                decryptFile(filePath, key, outFilePath=os.path.join(outFolderPath, file))
    except PermissionError as e:
        print("Error: Permission Denied.")
