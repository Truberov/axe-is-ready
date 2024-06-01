FROM python:3.10
LABEL authors="truberov"

WORKDIR /code
COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./qna_service .

EXPOSE 8080
