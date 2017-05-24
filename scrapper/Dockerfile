# Use an official Python runtime as a base image
FROM python:2.7-slim

# Set the working directory to /scrapper
WORKDIR /scrapper

# Copy the current directory contents into the container at /scrapper
ADD . /scrapper

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run main.py when the container launches
CMD ["python", "main.py"]
