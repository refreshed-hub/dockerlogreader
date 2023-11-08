# Use the official Python image with Ubuntu as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y python3-pip

# Install Python libraries
RUN pip install --upgrade pip
RUN pip install Flask docker gunicorn

# Copy the folder from the host to the container's working directory
COPY . /app

# Optional: If you need to expose a specific port for Flask (replace 5000 with the appropriate port)
EXPOSE 8000

# Run the Flask app when the container starts
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "Logreader:app"]
