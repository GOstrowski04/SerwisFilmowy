
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DirectorIn(BaseModel):
    name: str
    birth_year: Optional[int]


class Director(DirectorIn):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")