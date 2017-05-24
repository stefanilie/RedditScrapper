# Use an official Python runtime as a base image
FROM python:2.7-slim

# Set the working directory to /flask
WORKDIR /flask

# Copy the current directory contents into the container at /flask
ADD . /flask

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run flask_daemon.py when the container launches
CMD ["python", "flask_daemon.py"]
