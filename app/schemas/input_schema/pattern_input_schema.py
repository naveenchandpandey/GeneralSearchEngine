from pydantic import BaseModel


class Pattern(BaseModel):
    description: str = None
    name: str = None
