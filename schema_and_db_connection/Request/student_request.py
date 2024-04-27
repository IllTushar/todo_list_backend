from pydantic import BaseModel


class UserRequest(BaseModel):
    name: str
    email: str
    description: str | None = None
