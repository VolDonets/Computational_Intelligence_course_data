-- Create Authors Table
CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    nationality VARCHAR(50)
);

-- Create Books Table (author_id removed)
CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    published_year INT
);

-- Create the Junction Table for Many-to-Many Relationship
CREATE TABLE book_authors (
    book_id INT REFERENCES books(book_id) ON DELETE CASCADE,
    author_id INT REFERENCES authors(author_id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, author_id)
);

-- Insert Mock Data into Authors
INSERT INTO authors (name, nationality) VALUES
('Isaac Asimov', 'American'),        -- author_id: 1
('Stanislaw Lem', 'Polish'),         -- author_id: 2
('Ursula K. Le Guin', 'American'),   -- author_id: 3
('Terry Pratchett', 'British'),      -- author_id: 4
('Neil Gaiman', 'British');          -- author_id: 5

-- Insert Mock Data into Books
INSERT INTO books (title, published_year) VALUES
('Foundation', 1951),                -- book_id: 1
('Solaris', 1961),                   -- book_id: 2
('The Left Hand of Darkness', 1969), -- book_id: 3
('I, Robot', 1950),                  -- book_id: 4
('Beowulf', 1000),                   -- book_id: 5
('Good Omens', 1990);                -- book_id: 6

-- Map Authors to Books
INSERT INTO book_authors (book_id, author_id) VALUES
(1, 1), -- Foundation by Isaac Asimov
(2, 2), -- Solaris by Stanislaw Lem
(3, 3), -- The Left Hand of Darkness by Ursula K. Le Guin
(4, 1), -- I, Robot by Isaac Asimov
(6, 5); -- Good Omens by Neil Gaiman

-- Note: Beowulf (book_id 5) is intentionally left out of the book_authors table
-- to represent that it has no known author.