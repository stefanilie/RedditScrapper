# We first setup the ubuntu environment
FROM ubuntu:14.04

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

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

ENTRYPOINT ["python"]

# Run flask_daemon.py when the container launches
CMD ["flask_daemon.py"]
