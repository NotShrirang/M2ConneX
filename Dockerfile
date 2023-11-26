FROM python:3.9
ENV ENV=prod
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
WORKDIR /opt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
