FROM python:3.10

WORKDIR /project

COPY . /project

RUN pip install -r requirements.txt

CMD python server.py
