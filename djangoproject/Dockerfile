# Okay - need to look at https://github.com/PHACDataHub/cpho-phase2/blob/main/server/Dockerfile for example when revisit
FROM python:3.9-slim

# Install libpq-dev
RUN apt-get update \
    && apt-get install -y libpq-dev

# Set environment variables
ENV PYTHONUNBUFFERED=1, PYTHONDONTWRITEBYTECODE=1

# Set dworking irectory in container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project over
COPY . .

# Expose port
EXPOSE 8000

# When container starts:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]