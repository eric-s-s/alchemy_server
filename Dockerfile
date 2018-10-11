FROM python:3.7
ADD . /code/
WORKDIR /code


ENV NAME zoo_server 

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["./run_server_docker.sh"]
