
from pydantic import BaseModel, ConfigDict, UUID4


class UserIn(BaseModel):
    email: str
    password: str


class User(UserIn):
    id: UUID4
    model_config = ConfigDict(from_attributes=True, extra="ignore")