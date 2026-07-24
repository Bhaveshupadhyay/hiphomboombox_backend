from pydantic import BaseModel
from typing import Optional, Union, List

class PostBase(BaseModel):
    title: str
    title_translate: str
    description: Optional[str] = None
    des: str
    des_translate: str
    portrait_image: str
    image: str
    video: Optional[str] = None
    link: Optional[str] = None
    categories: Optional[str] = None
    categories_id: Optional[int] = None
    social_media: str
    views: int = 0
    date: str
    comment_count: int = 0

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: Union[int, str]

    class Config:
        from_attributes = True

class PostsResponseData(BaseModel):
    today: List[PostResponse]
    yesterday: List[PostResponse]
    day_before_yesterday: List[PostResponse]

class PostsResponse(BaseModel):
    isSuccess: bool
    today: str
    yesterday: str
    day_before_yesterday: str
    data: PostsResponseData
