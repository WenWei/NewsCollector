FROM python:3.7.4-alpine3.10 AS base

RUN apk add --update --no-cache --virtual .build-deps \
        gcc \
        g++ \
        python-dev \
        libxml2 \
        libxml2-dev && \
    apk add libxslt-dev

RUN pip install cython


WORKDIR /app
COPY . /app
RUN rm -rf /app/data/*

RUN pip install --no-cache-dir -r requirements.txt 
RUN apk del .build-deps gcc musl-dev

EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["app.py"]
