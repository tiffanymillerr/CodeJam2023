# Use an official Python runtime as a parent image
#Base image, pulling from dockerhub
FROM python:3.9-slim 

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir paho-mqtt

# Run mqtt_client.py when the container launches
ENTRYPOINT ["python", "./mqtt_client.py"]
