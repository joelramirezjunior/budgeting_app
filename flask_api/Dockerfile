# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set working directory
WORKDIR /usr/src/app

# Set environment variables
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV FLASK_APP ./app/app.py  
# This assumes youll run flask from /usr/src/app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
