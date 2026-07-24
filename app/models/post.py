from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.client import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    title_translate = Column(String, nullable=False)
    description = Column(String, nullable=True)
    des = Column(Text, nullable=False)
    des_translate = Column(Text, nullable=False)
    portrait_image = Column(String, nullable=False)
    image = Column(String, nullable=False)
    video = Column(String, nullable=True)
    link = Column(String, nullable=True)
    categories = Column(String, nullable=True)  # Comma-separated category names
    categories_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    social_media = Column(String, nullable=False)  # Comma-separated handles/links
    views = Column(Integer, default=0, nullable=False)
    date = Column(String, index=True, nullable=False)  # Upload/Publish date string (YYYY-MM-DD)
    comment_count = Column(Integer, default=0, nullable=False)

    category = relationship("Category", back_populates="posts")
