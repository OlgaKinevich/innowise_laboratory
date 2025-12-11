"""
Module models.py
Contains SQLAlchemy models for managing a book library database.
Models:
    - Book: Represents the `books_collection` table with columns id, title, author, year.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine("sqlite:///books.db")
# Base class for all SQLAlchemy models
Base = declarative_base()

class Book(Base):
    """
      SQLAlchemy model for the `books_collection` table.
      Attributes:
          id (int): Unique identifier for the book, primary key.
          title (str): Book title, cannot be empty.
          author (str): Book author, cannot be empty.
          year (int | None): Publication year, optional.
      """
    __tablename__ = "books_collection"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String, nullable=False)
    author: str = Column(String, nullable=False)
    year: int | None = Column(Integer, nullable=True)

    def __repr__(self):
        """
        Returns a string representation of the Book object for debugging.

        """
        return (f"<Book(id = {self.id}, "
                f"title = {self.title}, "
                f"author = {self.author}, "
                f"year = {self.year})>")

Base.metadata.create_all(engine)
