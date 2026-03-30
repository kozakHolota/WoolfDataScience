USE LibraryManagement;

INSERT INTO authors (author_name)
VALUES
    ('Taras Shevchenko'),
    ('Lesya Ukrainka'),
    ('Ivan Franko'),
    ('George Orwell'),
    ('Jane Austen'),
    ('Mark Twain'),
    ('Ernest Hemingway'),
    ('Agatha Christie'),
    ('J.K. Rowling'),
    ('Stephen King');

INSERT INTO genres (genre_name)
VALUES
    ('Poetry'),
    ('Drama'),
    ('Classic'),
    ('Dystopian'),
    ('Romance'),
    ('Adventure'),
    ('Historical Fiction'),
    ('Detective'),
    ('Fantasy'),
    ('Horror');

INSERT INTO books (title, publication_year, author_id, genre_id)
VALUES
    ('Kobzar', 1840, 1, 1),
    ('Forest Song', 1911, 2, 2),
    ('Zakhar Berkut', 1883, 3, 7),
    ('1984', 1949, 4, 4),
    ('Pride and Prejudice', 1813, 5, 5),
    ('The Adventures of Tom Sawyer', 1876, 6, 6),
    ('The Old Man and the Sea', 1952, 7, 3),
    ('Murder on the Orient Express', 1934, 8, 8),
    ('Harry Potter and the Philosopher''s Stone', 1997, 9, 9),
    ('The Shining', 1977, 10, 10);

INSERT INTO users (username, email)
VALUES
    ('andrii', 'andrii@example.com'),
    ('olena', 'olena@example.com'),
    ('maksym', 'maksym@example.com'),
    ('iryna', 'iryna@example.com'),
    ('bohdan', 'bohdan@example.com');

INSERT INTO borrowed_books (book_id, user_id, borrow_date, return_date)
VALUES
    (1, 1, '2026-03-01 10:00:00', '2026-03-15 14:00:00'),
    (2, 2, '2026-03-02 11:30:00', '2026-03-16 12:00:00'),
    (3, 3, '2026-03-03 09:15:00', '2026-03-17 16:20:00'),
    (4, 4, '2026-03-04 14:45:00', '2026-03-18 10:10:00'),
    (5, 5, '2026-03-05 08:20:00', '2026-03-19 13:30:00'),
    (6, 1, '2026-03-06 12:00:00', '2026-03-20 15:00:00'),
    (7, 2, '2026-03-07 10:40:00', '2026-03-21 11:50:00'),
    (8, 3, '2026-03-08 16:10:00', '2026-03-22 17:25:00'),
    (9, 4, '2026-03-09 13:35:00', '2026-03-23 09:45:00'),
    (10, 5, '2026-03-10 15:25:00', '2026-03-24 18:00:00'),
    (1, 2, '2026-03-11 09:00:00', '2026-03-25 10:30:00'),
    (2, 3, '2026-03-12 11:10:00', '2026-03-26 14:15:00'),
    (3, 4, '2026-03-13 14:20:00', '2026-03-27 16:40:00'),
    (4, 5, '2026-03-14 10:50:00', '2026-03-28 12:35:00'),
    (5, 1, '2026-03-15 08:45:00', '2026-03-29 11:00:00'),
    (6, 2, '2026-03-16 13:15:00', '2026-03-30 15:20:00'),
    (7, 3, '2026-03-17 17:05:00', '2026-03-31 18:10:00'),
    (8, 4, '2026-03-18 09:30:00', '2026-04-01 10:45:00'),
    (9, 5, '2026-03-19 12:25:00', '2026-04-02 13:55:00'),
    (10, 1, '2026-03-20 14:40:00', '2026-04-03 16:05:00');
