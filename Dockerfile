FROM python:3.10.7
ENV PYTHONUNBUFFERED=1
WORKDIR /pms_app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


