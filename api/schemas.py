from pydantic import BaseModel

class RequestModel(BaseModel):
    prompt : str
    model : str
    thinking : bool

