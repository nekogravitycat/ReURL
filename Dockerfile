FROM python:3.11.0
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b 0.0.0.0:5000", "src.website:app"]
