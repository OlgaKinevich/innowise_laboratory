# Use Python 3.13 as the base image
FROM python:3.13
# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main FastAPI app
COPY main.py .
# Expose port 8080 for the app
EXPOSE 8080

# Start the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

