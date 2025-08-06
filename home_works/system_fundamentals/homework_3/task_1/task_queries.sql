SELECT 'Завдання №1';
SELECT fullname, email FROM users WHERE id = (SELECT id FROM users LIMIT 1);

SELECT 'Завдання №2';
SELECT title, description FROM tasks WHERE status_id IN (SELECT id FROM status WHERE name = 'completed');

SELECT 'Завдання №3';
UPDATE status SET name='in progress'
              WHERE id = (
              SELECT t.status_id
              FROM tasks t
                  RIGHT JOIN status s
                      ON t.status_id = s.id WHERE s.name = 'new' LIMIT 1);

SELECT 'Завдання №4';
SELECT fullname FROM users WHERE id NOT IN (SELECT user_id FROM tasks);

SELECT 'Завдання №5';
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
        'Caesar dixit',
        'Veni. Vidi. Vici.',
        (SELECT id FROM status WHERE name = 'new'),
        (SELECT id FROM users LIMIT 1)
       );

SELECT 'Завдання №6';
SELECT t.title AS title, t.description, u.fullname AS description
FROM tasks t  LEFT JOIN users u ON t.user_id = u.id
LEFT JOIN status s ON t.status_id = s.id
WHERE s.name != 'done';

SELECT 'Завдання №7';
DELETE FROM tasks WHERE id = (SELECT id FROM tasks LIMIT 1);

SELECT 'Завдання №8';
SELECT fullname, email FROM users WHERE email LIKE '%.org';

SELECT 'Завдання №9';
UPDATE users SET fullname = 'Іван Сірко'
WHERE id = (SELECT  id FROM users LIMIT  1);

SELECT 'Завдання №10';
SELECT s.name, COUNT(*) FROM tasks t
    LEFT JOIN status s ON t.status_id = s.id
                GROUP BY s.name;

SELECT 'Завдання №11';
SELECT u.fullname AS fullname,
       u.email AS email,
       t.title AS title,
       t.description AS description
FROM tasks t LEFT JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@example.com';

SELECT 'Завдання №12';
SELECT title FROM tasks WHERE description IS NULL;

SELECT 'Завдання №13';
SELECT DISTINCT u.fullname AS fullname, u.email AS email
FROM users u INNER JOIN tasks t on u.id = t.user_id
    LEFT JOIN status s on t.status_id = s.id
WHERE s.name = 'in progress';

SELECT 'Завдання №14';
SELECT u.fullname AS fullname,
       u.email AS email,
       COUNT(t.id)
FROM users u LEFT JOIN tasks t ON u.id = t.user_id GROUP BY u.id;