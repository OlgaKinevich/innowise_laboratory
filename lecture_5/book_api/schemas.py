"""
Module schemas.py

Contains Pydantic models for request and response validation of books.
This module defines the following models:
- BookRead: Used for returning book data (read operations).
- BookCreate: Used for creating a new book entry (create operations).
- BookUpdate: Used for updating existing book data (update operations).

Validation rules:
- Title and author cannot be empty strings.
- Year, if provided, must be a positive integer and cannot be in the future.
"""
from typing import Optional
from datetime import date

from pydantic import BaseModel, field_validator

class BookRead(BaseModel):
    """
    Schema for reading a book record.

    Attributes:
        id (int): Unique identifier of the book.
        title (str): Title of the book.
        author (str): Author of the book.
        year (Optional[int]): Publication year of the book.
    """
    id: int
    title: str
    author: str
    year: Optional[int]


    class Config:
        """
        Pydantic configuration for the model.
        """
    # Enables ORM mode to allow reading data from ORM objects directly
        orm_mode = True

class BookCreate(BaseModel):
    """
    Schema for creating a new book.

    Validation:
    - Title and author cannot be empty.
    - Year must be positive and cannot be in the future.
    """
    title: str
    author: str
    year: Optional[int] = None

    @field_validator("title", "author")
    @classmethod
    def not_empty(cls, v: str) -> str:
        """
        Ensure that title and author fields are not empty or whitespace only.
        """
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v

    @field_validator("year")
    @classmethod
    def valid_year(cls, v: Optional[int]) -> Optional[int]:
        """
        Validate that year is positive and not in the future.
        """
        if v is not None:
            if v < 0:
                raise ValueError("Year must be positive")
            if v > date.today().year:
                raise ValueError("Year cannot be in the future")
        return v

class BookUpdate(BaseModel):
    """
    Schema for updating an existing book.
    All fields are optional; only provided fields will be updated.
    Validation:
    - Title and author cannot be empty strings if provided.
    - Year, if provided, must be positive and cannot be in the future.
    """
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None


    @field_validator("title", "author")
    @classmethod
    def not_empty(cls, v: Optional[str]) -> Optional[str]:
        """
        Ensure that title and author fields are not empty if provided.
        """
        if v is not None and not v.strip():
            raise ValueError("Field cannot be empty")
        return v

    @field_validator("year")
    @classmethod
    def valid_year(cls, v: Optional[int]) -> Optional[int]:
        """
        Validate that year, if provided, is positive and not in the future.
        """

        if v is not None:
            if v < 0:
                raise ValueError("Year must be positive")
            if v > date.today().year:
                raise ValueError("Year cannot be in the future")
        return v
