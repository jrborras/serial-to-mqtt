# Use an official Python runtime as a parent image
FROM python:3.12.6-alpine3.20

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 1883 available to the world outside this container
EXPOSE 1883

# Run the Python script when the container launches
CMD ["python", "app.py"]

# Run this commnad to do tests only, comment prevous CMD command
# CMD ["tail", "-f", "/dev/null"] 