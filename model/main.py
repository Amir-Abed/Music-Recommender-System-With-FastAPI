from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from recommender import data_to_send, find_similar_songs

# initializing FastAPI
app = FastAPI()

# type of the content we recieve from app.js
class DataPayLoad(BaseModel):
    data:str

# mounting a static folder to server images, js files, etc
app.mount("/static", StaticFiles(directory="static", html=True),name="static")

# configuring jinja2 to use a specified directory for rendering templates
templates = Jinja2Templates(directory="templates")

# handling a GET request to render the main HTML template as a HTML response
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="website/main.html"
    )

# handling a GET request to return a predefined list as a JSON response
@app.get("/get_data")
async def get_data():
    return {"list": data_to_send}

# handling a POST request to process recieved data from app.js and returning similar songs
@app.post("/submit_file")
async def recieve_data(file:DataPayLoad):
    return find_similar_songs(file.data, 5)