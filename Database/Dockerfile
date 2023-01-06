FROM postgres:11-alpine
ENV POSTGRES_PASSWORD=docker
ENV POSTGRES_DB=sncf
ENV POSTGRES_USER=postgres
ADD sncf.sql /docker-entrypoint-initdb.d
