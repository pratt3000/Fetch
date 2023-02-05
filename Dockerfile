FROM python:3.8-slim-buster

RUN mkdir /code/

WORKDIR /code/

ADD . / /code/

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "main.py"]
