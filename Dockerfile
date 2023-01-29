FROM python:3.10

ENV PYTHONDONTWRIBYTECODE 1
ENV PYTHONUNMUFFERED 1

WORKDIR /usr/src/test

COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/test

EXPOSE 8000
#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

