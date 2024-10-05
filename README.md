# Serial to MQTT Data Bridge

This project implements a Python-based containerized application that reads JSON data from a serial port (`/dev/ttyACM0`), adds a timestamp, and publishes the data to an MQTT broker. The project uses Docker and Docker Compose for easy setup and deployment.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [How it Works](#how-it-works)
- [Getting Started](#getting-started)
  - [Clone the Repository](#clone-the-repository)
  - [Configuration](#configuration)
  - [Build and Run](#build-and-run)
- [Environment Variables](#environment-variables)
- [Adding a Timestamp](#adding-a-timestamp)
- [Docker Setup](#docker-setup)
  - [Dockerfile](#dockerfile)
  - [docker-compose.yml](#docker-composeyml)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before starting, make sure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure

```
.
├── Dockerfile            # Dockerfile to build the Python container
├── docker-compose.yml    # Docker Compose file to run the container
├── .env                  # Environment variables for MQTT configuration
├── app.py             # Main Python script to capture and send serial data
├── requirements.txt      # Python dependencies (pyserial, paho-mqtt)
└── README.md             # Project documentation
```

## How it Works

1. The script reads data from a serial device (e.g., `/dev/ttyACM0`) using `pyserial`.
2. The received data is expected to be in JSON format.
3. A timestamp is added to the JSON data if it is a dictionary (JSON object).
4. The data is published to an MQTT broker using `paho-mqtt`.
5. Non-JSON or invalid data is ignored.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/jrborras/serial-to-mqtt.git
cd serial-to-mqtt
```

### Configuration

1. Create a `.env` file to configure the MQTT connection:

   ```bash
   touch .env
   ```

2. Populate the `.env` file with your MQTT configuration:

   ```ini
   # .env file
   MQTT_BROKER=your_mqtt_broker_url
   MQTT_PORT=1883
   MQTT_TOPIC=your/topic
   MQTT_USERNAME=your_username
   MQTT_PASSWORD=your_password
   TIME_ZONE=UTC
   ```

### Build and Run

1. **Build the Docker image**:
   
   ```bash
   docker-compose build
   ```

2. **Run the container**:

   ```bash
   docker-compose up -d
   ```

3. **Stop the container**:

   ```bash
   docker-compose down
   ```

## Environment Variables

The `.env` file is used to store the configuration for the MQTT broker. The following variables need to be defined:

- `MQTT_BROKER`: The address of the MQTT broker.
- `MQTT_PORT`: The port of the MQTT broker (default is `1883`).
- `MQTT_TOPIC`: The MQTT topic where the data will be published.
- `MQTT_USERNAME`: The username for authenticating with the MQTT broker.
- `MQTT_PASSWORD`: The password for authenticating with the MQTT broker.
- `TIME_ZONE`: Your local time zone

## Adding a Timestamp

The Python script appends a UTC timestamp to the JSON data if it is a valid JSON dictionary. The timestamp is in ISO 8601 format and is added as a `timestamp` field to the JSON object.

Example:

**Original JSON Data**:
```json
{
  "temperature": 23.5,
  "humidity": 60
}
```

**JSON Data with Timestamp**:
```json
{
  "temperature": 23.5,
  "humidity": 60,
  "timestamp": "2024-10-03T15:18:25.123456Z"
}
```

## Docker Setup

### Dockerfile

The `Dockerfile` builds a minimal Python container that runs the `app.py`.

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 1883 available to the world outside this container
EXPOSE 1883

# Run the Python script when the container launches
CMD ["python", "app.py"]
```

### docker-compose.yml

The `docker-compose.yml` file defines the `mqtt-client` service, which runs the `app.py` in a container. The `.env` file is used to configure the MQTT connection.

```yaml
version: '3'
services:
  mqtt-client:
    build: .
    container_name: mqtt_client
    restart: unless-stopped
    devices:
      - "/dev/ttyACM0:/dev/ttyACM0" # Ensure the serial port is exposed
    env_file:
      - .env  # Reference the .env file here
    volumes:
      - ./app:/app  # Mount the working directory
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
