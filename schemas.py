from pydantic import BaseModel

class Driver_Pydantic(BaseModel):
    id: int
    lat: float
    lng: float