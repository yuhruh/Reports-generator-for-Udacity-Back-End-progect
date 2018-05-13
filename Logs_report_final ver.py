#!/usr/bin/env python
import psycopg2


def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor

    except:
        print ("Unable to connect to database")


question = {1: "1. What are the most popular three articles of all time?",
            2: "2. Who are the most popular article authors of all time?",
            3: "3. On which days did more than 1% of request lead to errors?"}

query_ending = {1: " views", 2: " views", 3: " %"}

# reporting tool of query statements- Q1 to Q3
query = {1: """SELECT title, count(*)
         AS views
    FROM articles
INNER JOIN log
ON log.path = CONCAT('/article/', articles.slug)
GROUP BY title
ORDER BY views DESC
LIMIT 3;""",
         2: """SELECT name, sum(views)
AS views
FROM authorsview
GROUP BY name
ORDER BY views DESC;""",
         3: """SELECT day, percent
FROM error_percent
WHERE percent > 1
ORDER BY percent DESC;"""}


def execute_query(query):
    db, cursor = connect()
    cursor.execute(query)
    results = cursor.fetchall()
    db.close
    return results


def print_result():
    for key in query:
        results = execute_query(query[key])
        print('\n' + question[key] + '\n')
        for result in results:
                    print('\t' + str(result[0]) + ' : ' +
            str(result[1]) + query_ending[key])

if __name__ == '__main__':
    print_result()