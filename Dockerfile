FROM python:3.7
ADD . /code/
WORKDIR /code


ENV NAME erictest1

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "-m", "zoo_server.flask_app"]
