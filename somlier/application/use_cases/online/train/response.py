from pydantic import BaseModel


class TrainResponse(BaseModel):
    run_id: str
    status: str
