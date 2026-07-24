from sqlalchemy import Column, Integer, String
from app.database import Base

class FeaturedPost(Base):
    __tablename__ = "featured_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    portrait_image = Column(String, nullable=False)
    image = Column(String, nullable=False)
