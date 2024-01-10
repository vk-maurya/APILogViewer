from fastapi import FastAPI, HTTPException,Depends, Request

from utils.custom_logger import log_obj,logger,LOG_FOLDER,LOG_FILE_NAME
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn 
from typing import Dict 
try:
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")
    security = HTTPBasic()
except Exception as e:
    logger.error(f"Error in creating FastAPI instance: {e}")
    exit() 

# sample users 
users = {
    "user1": {"password": "password1"},
    "user2": {"password": "password2"}
}


@app.get("/view_logs", response_class=HTMLResponse)
async def view_logs(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    user = authenticate_user(credentials)
    if user:
        with open(LOG_FOLDER+"/"+LOG_FILE_NAME, "r") as log_file:
            logs = log_file.readlines()
        return templates.TemplateResponse("log_viewer.html", {"request": request, "logs": logs})
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = users.get(credentials.username)
    if user and user["password"] == credentials.password:
        return user
    return None


@app.post("/tokenize")
async def tokenize_text(input_text: Dict):
    log_obj.newid()
    logger.info(f"Request: {input_text}")
    tokens = input_text['text'].split()
    logger.info(f"Response: {tokens}")
    return {"tokens": tokens}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)