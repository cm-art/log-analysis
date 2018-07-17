
# Log Analysys Project

This project answers three questions by querying the "news" database. 

Sample Output 
```
Report 1: What are the most popular three articles of all time?
+----------------------------------+------------+
|          Article Title           | View Count |
+----------------------------------+------------+
| Candidate is jerk, alleges rival |   338647   |
| Bears love berries, alleges bear |   253801   |
| Bad things gone, say good people |   170098   |
+----------------------------------+------------+

Report 2: Who are the most popular article authors of all time?
+------------------------+------------+
|      Author Name       | View Count |
+------------------------+------------+
|    Ursula La Multa     |   507594   |
| Rudolf von Treppenwitz |   423457   |
| Anonymous Contributor  |   170098   |
+------------------------+------------+

Report 3: On which days >1% of requests lead to errors?
+---------------+----------+
|      Date     | % Errors |
+---------------+----------+
| July 17, 2016 |   2.3%   |
+---------------+----------+
 ```

Running on psycopg2 and PrettyTable to display output. 
All SQL commands needed to be created as one command, no additional Views were created for this application. 

---

# Information collected from psql cli on DB scema 

## Authors 
 Column |  Type   |                      Modifiers
 --------+---------+------------------------------------------------------
  name   | text    | not null
  bio    | text    |
  id     | integer | not null default nextval('authors_id_seq'::regclass)

Indexes:
    "authors_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)


## Articles
  Column |           Type           |                       Modifiers
 --------+--------------------------+-------------------------------------------------------
  author | integer                  | not null
  title  | text                     | not null
  slug   | text                     | not null
  lead   | text                     |
  body   | text                     |
  time   | timestamp with time zone | default now()
  id     | integer                  | not null default nextval('articles_id_seq'::regclass)
Indexes:
    "articles_pkey" PRIMARY KEY, btree (id)
    "articles_slug_key" UNIQUE CONSTRAINT, btree (slug)
Foreign-key constraints:
    "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

## Log
  Column |           Type           |                    Modifiers
 --------+--------------------------+--------------------------------------------------
  path   | text                     |
  ip     | inet                     |
  method | text                     |
  status | text                     |
  time   | timestamp with time zone | default now()
  id     | integer                  | not null default nextval('log_id_seq'::regclass)
Indexes:
    "log_pkey" PRIMARY KEY, btree (id)
