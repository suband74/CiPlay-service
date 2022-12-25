FROM python:3.10 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean
RUN pip install --upgrade pip

WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY . .
ENV PYTHONPATH=.
