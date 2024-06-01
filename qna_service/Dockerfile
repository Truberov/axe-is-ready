FROM python:3.10

WORKDIR /code
COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./load_model.py .
RUN python load_model.py

COPY ./qna_service ./qna_service

EXPOSE 8080
