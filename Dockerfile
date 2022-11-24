FROM python:3.10

WORKDIR /code

COPY requirements.txt .env /code/

RUN python -m pip install -r requirements.txt

COPY . ./code