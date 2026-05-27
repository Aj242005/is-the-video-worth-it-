'''main server file for the project'''
from fastapi import FastAPI, Response, status
from models import ResponseModel,Yturl
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

@app.get("/chat",response_model=ResponseModel)
def chat(response: Response):
    '''This is just a basic chat endpoint regarding the provided chat.....'''
    response.status_code = status.HTTP_200_OK
    return ResponseModel(
        message="Chat endpoint - send a message to converse with the AI",
        status=200,
        relevent_info=None
    )