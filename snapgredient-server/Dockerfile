# Use the official Python image as base image
FROM python:3.9-slim


# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of the local directory into the container at /app
COPY . .


# Command to run the FastAPI server
CMD ["uvicorn", "main:app"]
