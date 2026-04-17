from pydantic import BaseModel


class ActionAccepted(BaseModel):
    status: str
    detail: str | None = None
