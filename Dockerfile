FROM python:3.7
ADD . /code/
WORKDIR /code


ENV NAME zoo_server 

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "-m", "zoo_server.flask_app", "zoodb"]
