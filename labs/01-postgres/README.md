# PostgreSQL Lab

## Goal

This lab introduces Docker Compose by deploying a PostgreSQL database with persistent storage.

The objective is to understand how Compose simplifies container management compared to long `docker run` commands.

## What I learned

I learned how to write a simple docker compose for having a postgres container

## Commands I used

docker compose up -d
docker compose down
docker volume 
docker image

## Notes

This is the starting point of my lab.

## Lessons Learned

- `POSTGRES_DB` creates the initial database.
- Initialization scripts (`init.sql`) are executed against that database on the first startup.
- If you connect with `psql` without specifying `-d`, you may end up in a different database than expected.