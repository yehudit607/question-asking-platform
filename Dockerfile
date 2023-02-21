# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=1234
ENV POSTGRES_DB=mydb
ENV DATABASE_URL=postgres://myuser:1234@postgres:5432/mydb

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose port 8000 for the Django development server
EXPOSE 8000

# Start the Django development server

ENTRYPOINT ["/bin/bash", "-c", "python manage.py runserver 0.0.0.0:${PORT}"]
