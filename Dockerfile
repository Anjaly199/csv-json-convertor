FROM python:3.6.9

RUN mkdir /app
ADD converter.py /app

WORKDIR /app

ENTRYPOINT ["python3"]
CMD ["converter.py"]
COPY  /data.csv /app/data.csv