FROM python:3.10

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY templates/* ./
COPY css/* ./
COPY img/* ./
COPY py/* ./

RUN pip install -r requirements.txt

EXPOSE 3000

ENTRYPOINT ["python", "main.py"]
