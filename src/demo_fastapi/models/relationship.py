"""
# 多对多关系表设计
https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many
https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#combining-association-object-with-many-to-many-access-patterns
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class BookAuthor(Base):
    __tablename__ = "book_author"
    book_id = Column(ForeignKey("book.id"), primary_key=True)
    author_id = Column(ForeignKey("author.id"), primary_key=True)
    blurb = Column(String, nullable=False)
    book = relationship("Book", back_populates="author_associations", lazy="selectin")
    author = relationship("Author", back_populates="book_associations", lazy="selectin")


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_associations = relationship("BookAuthor", back_populates="book", lazy="selectin")
    authors = relationship("Author", secondary="book_author", viewonly=True, lazy="selectin")


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    book_associations = relationship("BookAuthor", back_populates="author", lazy="selectin")
    books = relationship("Book", secondary="book_author", viewonly=True, lazy="selectin")
