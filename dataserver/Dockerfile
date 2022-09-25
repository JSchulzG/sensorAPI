From python:3.9
RUN apt-get update \
&& apt-get install build-essential -y \
&& pip install poetry

COPY ./pyproject.toml /sensorAPI/
WORKDIR /sensorAPI/
RUN poetry install

COPY ./dataserver /sensorAPI/dataserver
RUN poetry install
ENTRYPOINT poetry run uvicorn dataserver.application:application --reload --host 0.0.0.0 --port 8080