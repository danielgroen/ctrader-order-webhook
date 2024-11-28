# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files to container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask python-dotenv ctrader-open-api twisted service_identity

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
