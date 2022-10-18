FROM python:3.7
WORKDIR /client
COPY requirements.txt ./requirements.txt
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt