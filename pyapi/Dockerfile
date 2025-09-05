FROM python:latest
WORKDIR /app
COPY ./req.txt .
RUN pip install -r req.txt
COPY ./api.py .
CMD [ "python","api.py" ]
