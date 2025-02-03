FROM python:3.13-alpine3.20

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./Pipfile ./Pipfile.lock /app/

RUN pip install pipenv \
    && pipenv install

COPY ./backend /app/

EXPOSE 8000

CMD [ "pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000" ]
