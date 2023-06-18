FROM python:3.10

WORKDIR /code

COPY requirements.txt /code
RUN pip install -r requirements.txt

COPY converter.py /code
COPY main.py /code
COPY ./templates /code/templates

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port 8000

