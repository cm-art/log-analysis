#!/usr/bin/env python3

from prettytable import PrettyTable
import psycopg2


def query_db(query):
    DBNAME = "news"
    '''Connects to DB and runs Query'''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    data = c.fetchall()
    db.close()
    return data


def get_top3():
    print("\nReport 1: What are the most popular three articles of all time?")
    query = """
        SELECT articles.title, count(*) AS num
        FROM articles
        JOIN log ON log.path LIKE CONCAT('/article/%', articles.slug)
        GROUP BY articles.title
        ORDER BY num DESC
        LIMIT 3
    """
    data = query_db(query)
    top3_table = PrettyTable(['Article Title', 'View Count'])
    for k, v in data:
        top3_table.add_row([k, v])
    print(top3_table)


def get_top_author():
    print("\nReport 2: Who are the most popular article authors of all time?")
    query = """
        SELECT authors.name, count(*) AS num
        FROM authors
        JOIN articles ON authors.id = articles.author
        JOIN log ON log.path LIKE CONCAT('/article/%', articles.slug)
        GROUP BY authors.name
        ORDER BY num DESC
        LIMIT 3
    """
    data = query_db(query)
    popular_table = PrettyTable(['Author Name', 'View Count'])
    for k, v in data:
        popular_table.add_row([k, v])
    print(popular_table)


def get_error_day():
    print("\nReport 3: On which days >1% of requests lead to errors?")
    query = """
        SELECT total.day,
        ROUND(((errors.error_req * 1.0) / total.requests), 3) AS per
        FROM ( SELECT date_trunc('day', time) "day", count(*) AS error_req
            FROM log WHERE status NOT LIKE '200 OK'
            GROUP BY day
        ) AS errors
        JOIN ( SELECT date_trunc('day', time) "day", count(*) AS requests
            FROM log
            GROUP BY day
        ) AS total
        ON total.day = errors.day
        WHERE (ROUND(((errors.error_req*1.0) / total.requests), 3) > 0.01)
        ORDER BY per DESC;
    """
    data = query_db(query)
    errorday_table = PrettyTable(['Date', '% Errors'])
    for d in data:
        date = d[0].strftime('%B %d, %Y')
        errors = str(round(d[1]*100, 1)) + "%"
        errorday_table.add_row([date, errors])
    print(errorday_table)


print("Collecting Reports...")
get_top3()
get_top_author()
get_error_day()
