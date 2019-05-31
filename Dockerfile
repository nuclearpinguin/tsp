FROM python:3.7

RUN pip install --upgrade pip
RUN pip install -U pyopenssl
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
COPY gapp.py .
COPY ./app ./app
