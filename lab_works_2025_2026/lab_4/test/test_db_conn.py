import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import asyncio
from sqlmodel import select
from src.database import get_session, Book, Author


async def test_query():
    # Get the database session
    async for session in get_session():

        # Write a query using Python objects instead of raw SQL strings!
        # Let's find "Foundation" and see who wrote it
        # SQL script analog:
        # select *
        #   from books
        #  where title = 'Foundation'
        statement = select(Book).where(Book.title == "Foundation")
        result = await session.execute(statement)
        book = result.scalars().first()

        if book:
            print(f"Found Book: {book.title} ({book.published_year})")

            # Because of our Relationship setup, SQLModel can automatically fetch the authors
            # Note: For async, we usually need to explicitly load relationships,
            # but this proves the base object maps correctly.
            print("Successfully mapped the Book object!")


if __name__ == "__main__":
    asyncio.run(test_query())
