from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import json

# Load configurations from config.json
with open('config.json') as config_file:
    config = json.load(config_file)


    

app = FastAPI()

# Replace 'mqtt_data' with your actual directory name where the files are saved
FILES_DIRECTORY = "mqtt_data"

@app.get("/files")
async def list_files():
    """
    Endpoint to list all files in the directory
    """
    files = []
    for filename in os.listdir(FILES_DIRECTORY):
        files.append(filename)
    return files

@app.get("/files/{filename}", response_class=FileResponse)
async def get_file(filename: str):
    """
    Endpoint to download a specific file
    """
    file_path = os.path.join(FILES_DIRECTORY, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")
