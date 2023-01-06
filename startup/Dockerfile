FROM python:latest

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY utils.py .

CMD ["python", "./utils.py"]