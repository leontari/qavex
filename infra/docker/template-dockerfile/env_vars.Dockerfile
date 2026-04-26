# syntax=docker.io/docker/dockerfile:1.3
FROM python:3.13-slim

WORKDIR /code

# Install production dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Install dev dependencies only in development
COPY ./requirements-dev.txt /code/requirements-dev.txt
RUN if [ "$ENVIRONMENT" = "development" ] ; then pip install -r /code/requirements-dev.txt ; fi

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
