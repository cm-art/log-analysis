#!/usr/bin/env python3

from prettytable import PrettyTable
import psycopg2


class DBQuery:
    """Connects to DB"""
    DBNAME = "news"

    def __init__(self):
        self.conn = psycopg2.connect(database=self.DBNAME)
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def get_top3(self):
        """Collect report #1 - Top 3 articles by querying the DB"""
        print("\nReport 1: What are the most popular articles of all time?")
        query = """
            SELECT articles.title, count(*) AS num
            FROM articles
            JOIN log ON log.path = '/article/' || articles.slug
            GROUP BY articles.title
            ORDER BY num DESC
            LIMIT 3
        """
        self.cur.execute(query)
        data = self.cur.fetchall()
        top3_table = PrettyTable(['Article Title', 'View Count'])
        for k, v in data:
            top3_table.add_row([k, v])
        print(top3_table)

    def get_top_author(self):
        """Collect report #2 - Top 3 popular authors by querying the DB"""
        print("\nReport 2: Who are the most popular authors of all time?")
        query = """
            SELECT authors.name, count(*) AS num
            FROM authors
            JOIN articles ON authors.id = articles.author
            JOIN log ON log.path = '/article/' || articles.slug
            GROUP BY authors.name
            ORDER BY num DESC
            LIMIT 3
        """
        self.cur.execute(query)
        data = self.cur.fetchall()
        popular_table = PrettyTable(['Author Name', 'View Count'])
        for k, v in data:
            popular_table.add_row([k, v])
        print(popular_table)

    def get_error_day(self):
        """Collect report #3 - Days where >1% of requests lead to errors"""
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
        self.cur.execute(query)
        data = self.cur.fetchall()
        errorday_table = PrettyTable(['Date', '% Errors'])
        for k, v in data:
            errorday_table.add_row([k, v])
        print(errorday_table)


if __name__ == '__main__':
    print("Collecting Reports...")
    db = DBQuery()
    db.get_top3()
    db.get_top_author()
    db.get_error_day()
