FROM python:3.9-slim

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["app.py"]
