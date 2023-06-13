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

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Set executable permissions for the entrypoint script
RUN chmod +x /entrypoint.sh

# Specify the entrypoint script as the container entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Expose port
EXPOSE 8080

# When container starts:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

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