#!/usr/bin/env python3

from prettytable import PrettyTable
import psycopg2


def query_db(query):
    """Connects to DB and runs Query"""
    DBNAME = "news"
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    data = c.fetchall()
    db.close()
    return data


def get_top3():
    """Collect report #1 of the top 3 popular articles by querying the DB"""
    print("\nReport 1: What are the most popular three articles of all time?")
    query = """
        SELECT articles.title, count(*) AS num
        FROM articles
        JOIN log ON log.path = '/article/' || articles.slug
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
    """Collect report #2 of the top 3 popular authors by querying the DB"""
    print("\nReport 2: Who are the most popular article authors of all time?")
    query = """
        SELECT authors.name, count(*) AS num
        FROM authors
        JOIN articles ON authors.id = articles.author
        JOIN log ON log.path = '/article/' || articles.slug
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
    """Collect report #3 of the days where >1% of requests lead to errors"""
    print("\nReport 3: On which days >1% of requests lead to errors?")
    query = """
        SELECT to_char(total.day, 'FMMonth DD, YYYY'),
        ROUND(((errors.error_req * 100.0) / total.requests), 2) AS per
        FROM ( SELECT time::date AS day, count(*) AS error_req
            FROM log WHERE status NOT LIKE '200 OK'
            GROUP BY day
        ) AS errors
        JOIN ( SELECT time::date AS day, count(*) AS requests
            FROM log
            GROUP BY day
        ) AS total
        ON total.day = errors.day
        WHERE (ROUND(((errors.error_req * 100.0) / total.requests), 2) > 1)
        ORDER BY per DESC;
    """
    data = query_db(query)
    errorday_table = PrettyTable(['Date', '% Errors'])
    for k, v in data:
        errorday_table.add_row([k, v])
    print(errorday_table)

if __name__ == '__main__':
    print("Collecting Reports...")
    get_top3()
    get_top_author()
    get_error_day()
