# Docker: Containerized Java Web Application with Tomcat, MySQL, Memcached, and RabbitMQ

This example demonstrates running a Java web application using a containerized approach.
The application is built and deployed with `Maven` on a `Tomcat` server, and relies on `MySQL`, `Memcached`, and `RabbitMQ`. An `Nginx` container acts as the web frontend.

#### Containers

The `docker-compose.yaml` file defines the following services:
- `vprodb` - MySQL database
- `vprocache01` - Memcached
- `vprodmq01` - RabbitMQ
- `vproapp` - Java application (Tomcat + Maven build)
- `vproweb` - Nginx web server


### Usage

#### Build images

```bash
docker compose build
```

Check that the images were built:

```bash
docker images --filter=reference='vprocontainers/*'
```
#### Run containers

```bash
docker compose up -d
```
List running containers:

```bash
docker ps
```

If needed: rebuild and restart:

```bash
docker compose up --build -d
```

#### Access the application

Visit: http://localhost

Login credentials:

- **Username**: `admin_vp`
- **Password**: `admin_vp`


#### Cleanup
To stop and remove all containers, networks, and resources created by Compose:

```bash
docker compose down
```
