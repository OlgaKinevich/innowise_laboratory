"""
main.py

FastAPI application for managing books using SQLAlchemy ORM.

Provides CRUD operations for books:
- Create a book
- Read all books
- Update a book
- Delete a book
- Search books by title, author, or year

Dependencies:
- SQLAlchemy for database interaction
- Pydantic models for request/response validation

Type hints and docstrings are included for clarity and IDE support.
"""
from typing import Generator, List, Optional, Type
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session, sessionmaker

from models import Book, engine
from schemas import BookRead, BookUpdate, BookCreate

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a SQLAlchemy session to path operations.

    Yields:
        Session: SQLAlchemy session object.

    Usage in FastAPI endpoint:

        from fastapi import Depends
        from sqlalchemy.orm import Session

        @app.get("/books/")
        def read_books(db: Session = Depends(get_db)):
            books = db.query(Book).all()
            return books

    Notes:
        - Session is automatically closed after the request.
        - Use `yield` to provide session and ensure proper cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

def check_book(book_id: int, db: Session) -> Book:
    """
    Verify that a book exists in the database.

    Args:
        book_id (int): ID of the book to check.
        db (Session): SQLAlchemy session.

    Returns:
        Book: The book object if found.

    Raises:
        HTTPException: If the book is not found (404).
    """
    book: Optional[Book] = db.query(Book).filter(book_id == Book.id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book


@app.post("/books/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def add_book(book: BookCreate, db: Session = Depends(get_db)) -> Book:
    """
    Add a new book to the database.

    Args:
        book (BookCreate): Book creation data.
        db (Session): Database session dependency.

    Returns:
        Book: The newly created book.
    """
    new_book = Book(title=book.title, author=book.author, year=book.year)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books/", response_model=List[BookRead], status_code=status.HTTP_200_OK)
def get_all_books(db: Session = Depends(get_db)) -> list[Type[Book]]:
    """
    Retrieve all books from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        List[Book]: List of all books.
    """
    books = db.query(Book).all()
    return books

@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
def delete_books(book_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Delete a book by ID.

    Args:
        book_id (int): ID of the book to delete.
        db (Session): Database session dependency.

    Returns:
        dict: Message indicating successful deletion.
    """
    book = check_book(book_id, db)
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

@app.put("/books/{book_id}", response_model=BookRead, status_code=status.HTTP_200_OK)
def update_book_details(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    """
    Update details of an existing book.

    Args:
        book_id (int): ID of the book to update.
        book_update (BookUpdate): Updated book data.
        db (Session): Database session dependency.

    Returns:
        Book: The updated book object.
    """
    book = check_book(book_id, db)
    if book_update.title is not None:
        book.title = book_update.title
    if book_update.author is not None:
        book.author = book_update.author
    if book_update.year is not None:
        book.year = book_update.year
    db.commit()
    db.refresh(book)
    return book

@app.get("/books/search/", response_model=List[BookRead], status_code=status.HTTP_200_OK)
def search_books(title : str | None = None,
                 author : str | None = None,
                 year : int | None = None,
                 db: Session = Depends(get_db)) -> list[Type[Book]]:
    """
    Search for books by title, author, or year.

    Args:
        title (Optional[str]): Partial or full book title.
        author (Optional[str]): Partial or full author name.
        year (Optional[int]): Year of publication.
        db (Session): Database session dependency.

    Raises:
        HTTPException: If no search parameters are provided (400).

    Returns:
        List[Book]: List of books matching the search criteria.
    """
    if not title and not author and not year:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide title or author or year to search"
        )
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if year is not None:
        query = query.filter(year == Book.year)
    return query.all()
