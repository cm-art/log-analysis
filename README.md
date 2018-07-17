
# Log Analysys Project

This project answers three questions by querying the "news" database. 

Running on psycopg2 and PrettyTable to display output. 
All SQL commands needed to be created as one command, no additional Views were created for this application. 

## Creating the Environment to run this program. 
---
This project requires a linux environment running python3 with a few additions. 
The setup I used runs a Vagrant with a VirtualBox VM solution which take a few steps to setup. 

### Setting up Virtual Environment for News DB
1. [Install Vagrant](https://www.vagrantup.com/downloads.html)
2. [Install VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
3. [Download and copy the VM from Udacity](https://github.com/udacity/fullstack-nanodegree-vm)
4. [Download the News Database here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
5. Create your virtual environment
  * Start your VM by running `vagrant up`
  * SSH into your VM by running `vagrant ssh`
  * Change Directory into /vagrant and use Git to clone in this reporting tool. 
  * `git clone https://github.com/cm-art/log-analysis.git`
6. Unzip the data to get the newsdata.sql file and copy it into the /vagrant directory 
7. Load the data into the Database by running `psql -d news -f newsdata.sql`
8. Change directory to /vagrant/log-analysis and then Run the Report `python3 py_report.py

---
Expected Output (_this can also be found in sample_output.txt_)
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
