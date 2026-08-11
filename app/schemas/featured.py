from pydantic import BaseModel
from typing import Union

class FeaturedPostBase(BaseModel):
    title: str
    portrait_image: str
    image: str

class FeaturedPostCreate(FeaturedPostBase):
    pass

class FeaturedPostResponse(BaseModel):
    id: Union[int, str]
    title: str
    portrait_image: str
    image: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Culture Box Feature",
                "portrait_image": "images/feature-portrait.jpg",
                "image": "images/feature-landscape.jpg"
            }
        }
