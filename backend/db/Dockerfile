# There is usually no need in custom Dockerfile.
# The official image is the best place to start.
# Still if we need a custom init, then something like this can be done:
FROM postgres:16

COPY schema.sql /docker-entrypoint-initdb.d/
COPY migrations/ /docker-entrypoint-initdb.d/migrations/
