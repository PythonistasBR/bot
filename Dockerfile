FROM python:alpine
WORKDIR /app
ADD . /app
RUN pip install pipenv && pipenv install --system --deploy
EXPOSE 5000
CMD flask run --host 0.0.0.0
