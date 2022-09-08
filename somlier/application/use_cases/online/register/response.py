from pydantic import BaseModel


class RegisterResponse(BaseModel):
    model_version: str
    message: str
