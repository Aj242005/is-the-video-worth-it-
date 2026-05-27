'''this is just basic model definations for the main.py 
file and created after a cry coz liniter was screaming'''

from typing import Annotated, Optional, Any, List
from pydantic import BaseModel, Field

class ResponseModel(BaseModel):
    """Response model containing a message, status, and optional relevant info."""
    message : Annotated[
        str,
        Field(
            default="~No Text was provided~",
            description="message to return on the route back -> user"
        )
    ]
    status : Annotated[
        int,
        Field(
            default=200,description="This is an HTTP status code --> use wisely"
        )
    ]
    relevent_info : Optional[
        Annotated[
            Any,
            Field(
                description='''This normal return imp. stuff when needed''',
                default = None
            ),

        ]
    ]
class Yturl(BaseModel):
    """Model containing a YouTube video URL."""
    url: Annotated[str, Field(description="This is the url of youtube video.")]
    context: Annotated[
        List[Any],
        Field(
            default=[],
            description="This is the chat history of the given thing"
        ),
    ]
    chat : Annotated[
        str,
        Field(
            default="complete any pending task based on the context else do nothing",
            description="This is a chat text message"
        )
    ]
