# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Expose the port where the app will run
EXPOSE 7860

# Start both backend and frontend
CMD ["bash", "-c", "uvicorn backend:app --host 0.0.0.0 --port 8000 & python frontend.py"]