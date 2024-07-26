# Image specification (lighter version of Python 3.9)
FROM python:3.9-slim

# Working directory on container
WORKDIR /app

# Copy requirements file on '/app' directory and install dipendencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy all files from host to '/app' on docker
COPY . .

# Copy the kickstart.sh script into the container
COPY kickstart.sh /app/kickstart.sh

# Make sure the kickstart.sh is executable
RUN chmod +x /app/kickstart.sh

# Set the entrypoint to the script
ENTRYPOINT ["/app/kickstart.sh"]
