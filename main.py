'''main server file for the project'''
from fastapi import FastAPI, Response, status
from dotenv import load_dotenv
from models import ResponseModel,Yturl
from controllers import handle_url_and_prompt
load_dotenv()
app = FastAPI()

@app.get("/",response_model=ResponseModel)
def home(response: Response):
    '''This is just the home route'''
    response.status_code = status.HTTP_200_OK
    return ResponseModel(
        message = "Welcome to the home page of talking with the ai",
        status=200,
        relevent_info=None
    )

@app.post("/chat",response_model=ResponseModel)
def chat(chat_object : Yturl, response: Response):
    '''This is just a basic chat endpoint regarding the provided chat.....'''
    response.status_code = status.HTTP_200_OK
    res = handle_url_and_prompt(chat_object)
    return ResponseModel(
        message="this is the given response by the Ai",
        status=200,
        relevent_info=res
    )
