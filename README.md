# Warehouse app

## Docker
`docker-compose up`

## PostgreSQL pgAdmin
    http://localhost:5050
    user: admin@admin.com
    password: password


## MySQL phpMyAdmin
    http://localhost:8081
    server: mysql
    user: admin
    password: password

## Run
`python3 src/window.py`

## TODO 
1. Create categories and goods tables in Postgres and Mysql
2. Copy-paste model.py classes (update database URL) for Postgres and Mysql. You'll have something like: SqliteCategory/Good, PostgresCategory/Good, MysqlCategory/Good
3. Export:
    - delete goods, then categories from second db
    - get categories and goods from first db
    - create new instances of second db with values from first db
4. Sqlite doesn't have Date field, but Postgres and Mysql do. I store dates in Mysql as UTC timestamp. This will be the only transformation.
5. Write logs to console, use PEP8 codestyle.