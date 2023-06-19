# Okay - need to look at https://github.com/PHACDataHub/cpho-phase2/blob/main/server/Dockerfile for example when revisit
FROM python:3.11-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

# # Install libpq-dev - not sure if 
# RUN apt-get update \
#     && apt-get install -y libpq-dev

# Set environment variables
ENV PYTHONUNBUFFERED=1 
# ENV PYTHONDONTWRITEBYTECODE=1

# # Set dworking irectory in container
# WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project over
COPY . .


# # Set executable permissions
# RUN chmod +x ./entrypoint.sh

# # Specify the entrypoint as the container entrypoint
# ENTRYPOINT ["./entrypoint.sh"]

# # Or Do this and remove entrypoint.sh
# # Apply database migrations
# RUN python manage.py makemigrations
# RUN python manage.py migrate

# # Expose port
# EXPOSE 8080

# # When container starts:
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 mysite.wsgi:application
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