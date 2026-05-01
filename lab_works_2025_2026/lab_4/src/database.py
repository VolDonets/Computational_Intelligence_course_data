from typing import List, Optional
from sqlalchemy.engine import URL
from sqlmodel import Field, Relationship, SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


# 1. The Junction Table (Many-to-Many Link)
class BookAuthorLink(SQLModel, table=True):
    __tablename__ = "book_authors"
    book_id: Optional[int] = Field(default=None, foreign_key="books.book_id", primary_key=True)
    author_id: Optional[int] = Field(default=None, foreign_key="authors.author_id", primary_key=True)


# 2. The Author Table
class Author(SQLModel, table=True):
    __tablename__ = "authors"
    author_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    nationality: Optional[str] = None

    # This creates the link back to books
    books: List["Book"] = Relationship(back_populates="authors", link_model=BookAuthorLink)


# 3. The Book Table
class Book(SQLModel, table=True):
    __tablename__ = "books"
    book_id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    published_year: Optional[int] = None

    # This creates the link to authors
    authors: List[Author] = Relationship(back_populates="books", link_model=BookAuthorLink)


# The connection string using the asyncpg driver and port 5433
DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username="mcp_user",
    password="M&1_V3r^_C9#pLeX_P@$s",  # SQLAlchemy will safely encode the # and @ symbols
    host="localhost",
    port=5433,
    database="mcp_database"
)

# Create the async engine
# echo=True prints the raw SQL to the console for learning!
# engine = create_async_engine(DATABASE_URL, echo=True)
engine = create_async_engine(DATABASE_URL, echo=False)


# A dependency function to provide database sessions
async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
