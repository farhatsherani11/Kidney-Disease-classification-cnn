FROM python:3.13.2-slim-buster  # Use official Python runtime as a parent image

RUN apt update -y && apt install awscli -y # Install AWS CLI
WORKDIR /app   # Set the working directory in the container

COPY . /app   # Copy the current directory contents into the container at /app
RUN pip install -r requirements.txt   # Install any needed packages specified in requirements.txt

CMD ["python3", "app.py"]  # Run app.py when the container launches