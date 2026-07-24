from pydantic import BaseModel
from typing import Union

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(BaseModel):
    id: Union[int, str]
    name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Rap"
            }
        }
