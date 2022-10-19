# FROM ubuntu:latest

# # Install python3
# RUN apt-get update
# RUN apt-get install -y python3.5 python3-pip
# RUN apt-get install -y libpq-dev python3-dev
FROM python:3.7
WORKDIR /app
RUN pip3 install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ENV HOME /app

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "600", "app.wsgi:application",  "--log-level","DEBUG"]
