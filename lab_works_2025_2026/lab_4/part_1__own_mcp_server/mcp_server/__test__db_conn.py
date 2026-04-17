import asyncio
from sqlmodel import select
from database import get_session, Book, Author


async def test_query():
    # Get the database session
    async for session in get_session():

        # Write a query using Python objects instead of raw SQL strings!
        # Let's find "Foundation" and see who wrote it
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