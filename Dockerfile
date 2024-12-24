FROM python:3.12

COPY . .
WORKDIR .
RUN python3 -m pip install -r requirements.txt
EXPOSE 4000

RUN python manage.py migrate

# Создание суперпользователя с автоматическими параметрами
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'root@example.com', '1')" | python manage.py shell

CMD ["python", "manage.py", "runserver", "0.0.0.0:4000"]
