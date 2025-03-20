# Specific alpine version for compatibility with the course
FROM python:3.9-alpine3.13

# Who maintains this image?
LABEL maintainer="won't tell you"

# Set the environment variable
# Don't buffer the output from python, print it directly to console
ENV PYTHONUNBUFFERED=1

# Commands
# Copy requirements
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# Copy the django app directory
COPY ./app /app
# Default directory that all commands are going to be run from in docker image
WORKDIR /app
# Expose port 8000 in the container
EXPOSE 8000

# this argument will be overriden to true when running through docker-compose
ARG DEV=false

# Runs all commands on alpine image at once. Doing that line by line would add image layer for every single cmd.
# This way keeps image light.
# What it does:
#   - new virtual environment (arguable not necessary but in corner cases the alpine image might have dependencies
#     conflicting with what we want to do here
#   - upgrade pip
#   - install posgresql-client (needed to connect to postgresql)
#   - install jpeg-dev (needed fgor Pillow)
#   - --virtual .file - virtual dependency package, to be removed later, packages are needed to build posgresql
#       adapter
#   - install requirements
#   - if DEV is true - install also dev requirements
#   - remove the /tmp directory - no extra dependencies, keeps image lean
#   - remove the dependencies used to build psycopg
#   - add user - not to use root user
#       -D		Don't assign a password
#       -H		Don't create home directory
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser -D -H django-user && \
    # add directories for media and statics
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    # change recursive owner of the directory
    chown -R django-user:django-user /vol &&\
    chmod -R 755 /vol

# Update PATH were executables are run
ENV PATH="/py/bin:$PATH"

# Switch user to, anytime we run something on image, it's run as that user
USER django-user