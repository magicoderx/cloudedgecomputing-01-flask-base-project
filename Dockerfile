# Image specification (lighter version of Python 3.8)
FROM python:3.8-slim

# Working directory on container
WORKDIR /app

# Copy requirements file on '/app' directory and install dipendencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy all files from host to '/app' on docker
COPY . .

# Run command 'flask run' accessible from all the interfaces
CMD ["flask", "run", "--host=0.0.0.0"]
