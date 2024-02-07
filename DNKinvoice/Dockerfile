# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code/
COPY . /code/

# Run database migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the Django application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "DNKinvoice.wsgi:application"]
