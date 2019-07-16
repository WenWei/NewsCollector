FROM python:3.7.4-alpine3.10

COPY . /app

RUN pip install Flask

# ENV FLASK_APP=proxycrawler.py
# ENV FLASK_ENV=development

WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["main.py"]
