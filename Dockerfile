# Use Python 3.11 as the parent image
FROM python:3.11

# Set working directory to app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 5500 for the server
EXPOSE 5500

# Run main.py when the container launches
CMD ["sudo", "python", "./main.py"]

