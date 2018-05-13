#Udacity Fullstack Developer Project : Logs Analysis
---------------------------------------------------------------------
Use python code to fetch desired information from news database in order to build an internal reporting tool that prints out report in plain text.
 

##Introduction

###The news database includes three tables:

- Authors table includes name, biography and id.
- Articles table includes author, title, slug, lead, body, time and id.
- Log table includes path, ip, method, status, time and id.

###This project will be got following results:

- The most popular three articles
- The most popular article authors
- On which days did more than 1% of request leads to errors

###Before Running:
You will need belowed tools

 * Python2 or 3
 * Virtual Box
 * Vagrant
 * Git or cmd

##Instructions

###Install Virtual Box/Vagrant Machine and Download Vagrant Machine
 * [Vagrant](https://www.vagrantup.com/), [Virtual Box](https://www.virtualbox.org/wiki/Downloads) and [vagrant machine file](https://drive.google.com/open?id=1suidFchiN9jYA8a8Xx9w2wABdBd3DBt3)

###Launch Virtual Box
 1. Launch **Virtual Box** by _Git_ or _cmd_ running `vagrant up`, and then `vagrant ssh`.

 2. You should see something like this as following picture in **Vagrant Up**![vagrant up image](https://i.imgur.com/0C4kCiM.png)
 ref: [Udacity: Intro to Programming](https://classroom.udacity.com/nanodegrees/nd000/parts/b910112d-b5c0-4bfe-adca-6425b137ed12/modules/a3a0987f-fc76-4d14-a759-b2652d06ab2b/lessons/0aa64f0e-30be-455e-a30d-4cae963f75ea/concepts/eaf58af6-a1fa-43a0-b4de-311e04689748)

 3. You will see something like this as following picture in **Vagrant ssh**![Vagrant SSH image](https://i.imgur.com/dhuAeqZ.png)
 ref: [Udacity: Intro to Programming](https://classroom.udacity.com/nanodegrees/nd000/parts/b910112d-b5c0-4bfe-adca-6425b137ed12/modules/a3a0987f-fc76-4d14-a759-b2652d06ab2b/lessons/0aa64f0e-30be-455e-a30d-4cae963f75ea/concepts/a9cf98c8-0325-4c68-b972-58d5957f1a91)

###Required command to load data => connect to database => explore the tables: 

 1. You need to download the newsdata.zip file then unzip. This inside file includes newsdata.sql. Put it into the vagrant directory which is shared with Virtual Box.
 2. Load data: cd into the vagrant directory and use the command `psql -d news -f newsdata.sql` to load data.

 3. Connect to database:  `psql news` to connect to database.
 4. Explore the tables: `\dt` which can list the available tables in the database
 5. Show the particular table schema: `\d _table name_`

 6. If you encountered belowed situation:
 
> perl: warning: setting locale failed

>> you could refer this website [here](https://askubuntu.com/questions/162391/how-do-i-fix-my-locale-issue) to fix it.


###Functions in Logs_report.py:

 1. `connect()`: Connets to the news database and returns to the connection
 2. `execute_query()`: Store entire result set on the server and return all the result set
 3. `print_top_articles()`: Print out the top 3 articles in plain text
 4. `print_top_authors()`: Print out the top 3 authors in plain text
 5. `print_errors_over_one()`: Print out which days did more than 1% of request leads to error


###Views to be created:

  * Top Authors:
  ```psql
  CREATE VIEW authorsview
AS SELECT authors.name, articles.title, count(*)
AS views
FROM articles
INNER JOIN log
ON log.path = CONCAT('/article/', articles.slug)
INNER JOIN authors
ON articles.author = authors.id
GROUP BY name, title
ORDER BY views DESC;
  ```

  
  * Errors over One:
  ```psql
  CREATE VIEW request
AS SELECT substring (CAST(log.time AS text), 0, 11)
AS day, count(*)
AS request
FROM log
GROUP BY day;
  ```
  ```psql
  CREATE VIEW error
AS SELECT substring (CAST(log.time AS text), 0, 11)
AS day, count(status)
AS error
FROM log
WHERE status = '404 NOT FOUND'
GROUP BY day;
   ```
  ```psql
  CREATE VIEW error_request
AS SELECT request.day, error.error, request.request
FROM error
INNER JOIN request
ON request.day = error.day
GROUP BY request.day, error.error, request.request;
  ``` 
  ```psql
  CREATE VIEW error_percent
AS SELECT day, ROUND(((error AS float)*100/request), 2)
AS percent
FROM error_request
GROUP BY day, error, request
ORDER BY percent DESC;
  ```

###Running the queries:

> `$ python Logs_report.py`

* Output Report:
![Output Report](https://i.imgur.com/zoeG122.png)
