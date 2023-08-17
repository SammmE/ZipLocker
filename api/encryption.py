import os
from cryptography.fernet import Fernet
import zipfile

def compressFolder(folder_path, zip_file_name, compLvl=9):
    zip_file = zipfile.ZipFile(zip_file_name, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=compLvl)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            zip_file.write(os.path.join(root, file))
    zip_file.close()

def decompressFolder(zip_file_name, extract_folder):
    zip_file = zipfile.ZipFile(zip_file_name, 'r')
    zip_file.extractall(extract_folder)
    zip_file.close()

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

            if not os.path.exists(outFolderPath):
                os.mkdir(outFolderPath)

            encryptFile(filePath, key, outFilePath=os.path.join(outFolderPath, file))

def decryptFolder(folderPath, key, outFolderPath):
    try:
        if outFolderPath is None:
            outFolderPath = folderPath
        for root, dirs, files in os.walk(folderPath):
            for file in files:
                filePath = os.path.join(root, file)

                if not os.path.exists(outFolderPath):
                    os.mkdir(outFolderPath)


                decryptFile(filePath, key, outFilePath=os.path.join(outFolderPath, file))
    except PermissionError as e:
        print("Error: Permission Denied.")

if __name__ == "__main__":
    compressFile("./test/test.txt", "./test.zip")