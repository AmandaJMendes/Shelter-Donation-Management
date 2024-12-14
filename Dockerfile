# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Copy the rest of the application code into the container
COPY . .

# Install JavaScript dependencies
RUN cd Frontend && npm install

# Install ESLint globally
RUN npm install -g eslint

# Copy the script into the container
COPY docker_checks.sh .

# Run the script
CMD ["sh", "-c", "./docker_checks.sh"]