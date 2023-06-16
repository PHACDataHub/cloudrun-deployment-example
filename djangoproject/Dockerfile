# Okay - need to look at https://github.com/PHACDataHub/cpho-phase2/blob/main/server/Dockerfile for example when revisit
FROM python:3.9-slim

# # Install libpq-dev - not sure if 
# RUN apt-get update \
#     && apt-get install -y libpq-dev

# Set environment variables
ENV PYTHONUNBUFFERED=1, PYTHONDONTWRITEBYTECODE=1

# Set dworking irectory in container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project over
COPY . .

# Set executable permissions
RUN chmod +x ./entrypoint.sh
RUN chmod +x ../cloud_sql_proxy

# Specify the entrypoint as the container entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# # Or Do this and remove entrypoint.sh
# # Apply database migrations
# RUN python manage.py makemigrations
# RUN python manage.py migrate

# # Expose port
# EXPOSE 8080

# # When container starts:
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
ENV PORT 8080
CMD sh -c "../cloud-sql-proxy phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:hello-world-instance & && gunicorn --bind :$PORT --workers 3 djangoproject.wsgi"
# CMD gunicorn --bind :$PORT --workers 3 djangoproject.wsgi
# #---------------------
# FROM python:3.9-slim as compiler
# ENV PYTHONUNBUFFERED 1, PYTHONDONTWRITEBYTECODE=1

# WORKDIR /app/

# RUN python -m venv /opt/venv
# # Enable venv
# ENV PATH="/opt/venv/bin:$PATH"

# COPY ./requirements.txt /app/requirements.txt
# RUN pip install -Ur requirements.txt

# FROM python:3.9-slim as runner
# WORKDIR /app/
# COPY --from=compiler /opt/venv /opt/venv

# # Enable venv
# ENV PATH="/opt/venv/bin:$PATH"
# COPY . /app/
# # CMD ["python", "app.py", ]
# # Expose port
# EXPOSE 8087

# # When container starts:
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8087"]