FROM django
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -U -r requirements.txt

COPY ./ .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]