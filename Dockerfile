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
# Copy the django app directory
COPY ./app /app
# Default directory that all commands are going to be run from in docker image
WORKDIR /app
# Expose port 8000 in the container
EXPOSE 8000

# Runs all commands on alpine image at once. Doing that line by line would add image layer for every single cmd.
# This way keeps image light.
# What it does:
#   - new virtual environment (arguable not necessary but in corner cases the alpine image might have dependencies
#     conflicting with what we want to do here
#   - upgrade pip
#   - install requirements
#   - remove the /tmp directory - no extra dependencies, keeps image lean
#   - add user - not to use root user
#       -D		Don't assign a password
#       -H		Don't create home directory
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser -D -H django-user

# Update PATH were executables are run
ENV PATH="/py/bin:$PATH"

# Switch user to, anytime we run something on image, it's run as that user
USER django-user