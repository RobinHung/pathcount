# PathCount

In this project, there will be two Docker containers, one for Flask Server and one for PostgreSQL database, communicating with each other. The Server can accept GET requests, and update that GET request path into the Postgres database, then returning all the existing request paths and how many time those paths have been requested.


![demo](https://preview.ibb.co/d6DR50/Screen-Shot-2018-11-01-at-4-11-04-PM.png)

## Instructions

```bash
# List current network default
$ docker network ls

# Create new docker network
$ docker network create <NAME>
```

### PostgreSQL

Be sure to use `cd postgres` to  navigate to the postgres directory!

```bash
$ docker run --network pgnet --name pg-db -e POSTGRES_PASSWORD=password -d postgres

# Lookup that your container IP
$ docker container inspect mypg -f '{{.NetworkSettings.Networks.pgnet.IPAddress}}'
172.20.0.2

# Initialize the database
$ docker run -i --network pgnet -e PGPASSWORD=password postgres psql -h <IP_ADDRESS> -U postgres < init.sql

# Postgres console
$ docker exec -it pg-db psql -U postgres

postgres=# \dt

postgres=# SELECT * FROM pathcount;
```

### Flask

`cd flask-server` first!

```bash
# Build the docker image
$ docker build pathcount-serve .

$ docker run --network pgnet --name pathcount -p 9090:8080 pathcount-server
```
