# Use Python 3.11 as the parent image
FROM python:3.11

# Set working directory to app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Initialize and update submodules
RUN git submodule update --init --recursive

# Expose port 5500 for the server
EXPOSE 5500

# Run main.py when the container launches
CMD ["python", "./main.py"]

