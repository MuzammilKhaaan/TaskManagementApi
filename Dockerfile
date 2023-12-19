FROM python:3.8-slim


WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev gcc


ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient -lpthread -lz -lm -lrt -ldl"


COPY requirements.txt /app


RUN pip install --trusted-host pypi.python.org -r requirements.txt


EXPOSE 5000

ENV NAME World

COPY ./app /app

CMD ["python", "router.py"]