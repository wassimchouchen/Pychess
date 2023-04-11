FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /Pychess

COPY ./requirements.txt /Pychess/Chess_api/requirements.txt 
RUN pip install -r /Pychess/Chess_api/requirements.txt

COPY . /Pychess

CMD ["python", "manage.py", "runserver"]