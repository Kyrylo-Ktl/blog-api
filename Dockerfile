# pull official base image
FROM python:3.8

# set work directory
WORKDIR /usr/src/app/project

# set system-wide environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy dependencies list
COPY pyproject.toml poetry.lock /usr/src/app/

# install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# copy project
COPY project /usr/src/app/