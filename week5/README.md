# Task 2：Create database and table in MySQL server

## 2-1 Create database

```sql
CREATE DATABASE website;
USE website;
SELECT DATABASE();
```

## Result 2-1

![Task 2-1 Result](./img/2-1.png)

## 2-2 Create table

```sql
CREATE TABLE member (
id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
follower_count INT UNSIGNED NOT NULL DEFAULT 0,
time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
SHOW TABLES;
DESCRIBE member;
```

## Result 2-2

![Task 2-2 Result](./img/2-2.png)

# Task 3: SQL CRUD

## 3-1

INSERT a new row to the member table where name, email and password must be set to test , test@test.com , and test . INSERT additional 4 rows with arbitrary data.

```sql
INSERT INTO member (name, email, password, follower_count)
VALUES ('test', 'test@test.com', 'test', 10);

INSERT INTO member (name, email, password, follower_count)
VALUES
('Alice', 'alice@example.com', 'alice123', 50),
('Bob', 'bob@example.com', 'bob123', 30),
('Chris', 'chris@example.com', 'chris123', 80),
('Daisy', 'daisy@example.com', 'daisy123', 20);
```

## Result 3-1

![Task 3-1](./img/3-1.png)

## 3-2

SELECT all rows from the member table.

```sql
SELECT * FROM member;
```

## Result 3-2

![Task 3-2](./img/3-2.png)

## 3-3

SELECT all rows from the member table, in descending order of time.

```sql
SELECT * FROM member
ORDER BY time DESC;
```

## Result 3-3

![Task 3-3](./img/3-3.png)

## 3-4

SELECT total 3 rows, second to fourth, from the member table, in descending order of time.

```sql
SELECT * FROM member
ORDER BY time DESC
LIMIT 3 OFFSET 1;
```

## Result 3-4

![Task 3-4](./img/3-4.png)

## 3-5

SELECT rows where email equals to test@test.com .

```sql
SELECT * FROM member
WHERE email = 'test@test.com';
```

## Result 3-5

![Task 3-5](./img/3-5.png)

## 3-6

SELECT rows where name includes the es keyword.

```sql
SELECT * FROM member
WHERE name LIKE '%es%';
```

## Result 3-6

![Task 3-6](./img/3-6.png)

## 3-7

SELECT rows where email equals to test@test.com and password equals to test .

```sql
SELECT * FROM member
WHERE email = 'test@test.com'
AND password = 'test';
```

## Result 3-7

![Task 3-7](./img/3-7.png)

## 3-8

UPDATE data in name column to test2 where email equals to test@test.com .

```sql
UPDATE member
SET name = 'test2'
WHERE email = 'test@test.com';
```

## Result 3-8

![Task 3-8](./img/3-8.png)
