from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from demo_fastapi.core.deps import get_db, get_db_async
from demo_fastapi.models import Author, Book, BookAuthor

router = APIRouter()


@router.post("/authors", summary="创建作者")
async def create_author(db: AsyncSession = Depends(get_db_async)):
    author_db = Author(
        name="test2",
    )
    db.add(author_db)
    await db.commit()
    await db.refresh(author_db)
    return author_db


@router.post("/books", summary="创建图书")
async def create_book(db: AsyncSession = Depends(get_db_async)):
    book_db = Book(
        title="test2",
    )
    db.add(book_db)
    await db.commit()
    await db.refresh(book_db)
    return book_db


class BookAuthorCreate(BaseModel):
    book_id: int
    author_id: int
    blurb: str | None = None


@router.post("/book_authors", summary="创建图书作者")
async def create_book_author(
    book_author: BookAuthorCreate, db: AsyncSession = Depends(get_db_async)
):
    book_author_db = BookAuthor(
        book_id=book_author.book_id,
        author_id=book_author.author_id,
        blurb=book_author.blurb,
    )
    db.add(book_author_db)
    await db.commit()
    await db.refresh(book_author_db)
    return book_author_db


@router.get("/book_authors/{id}", summary="获取某图书的所以作者")
async def get_authors_by_book_id_1(id: int, db: AsyncSession = Depends(get_db_async)):
    book_authors = await db.execute(
        select(BookAuthor)
        .options(joinedload(BookAuthor.book))
        .options(joinedload(BookAuthor.author))
        .where(BookAuthor.book_id == id)
    )
    # res = book_authors.scalars().all()
    return book_authors.scalars().all()


@router.get("/books/{id}", summary="获取某图书的所有作者")
async def get_authors_by_book_id(id: int, db: AsyncSession = Depends(get_db_async)):
    async with db.begin():
        result = await db.execute(
            select(Book)
            .options(joinedload(Book.authors))
            .options(joinedload(Book.author_associations))
            .where(Book.id == id)
        )
        book = result.scalars().unique().one_or_none()
        return dict(a=book.authors, b=book.author_associations)


@router.get("/authors/{id}", summary="获取某作者的所有图书")
async def get_books_by_author_id(id: int, db: AsyncSession = Depends(get_db_async)):
    result = await db.execute(
        select(Author).options(joinedload(Author.books)).where(Author.id == id)
    )
    author = result.scalars().unique().one_or_none()
    return dict(a=author.books, b=author.book_associations)


@router.get("/book_author/", summary="获取某作者的所有图书")
def get_book_authors(db: Session = Depends(get_db)):
    result = db.execute(
        select(BookAuthor)
        .where(BookAuthor.author_id == 1)
        .where(BookAuthor.book_id == 1)
    )
    book_author = result.scalars().one_or_none()
    return dict(book=book_author.book, author=book_author.author)
