# Use a base image that includes git and bash
FROM python:3.11-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Set the GIT_SSH_COMMAND environment variable to force HTTPS
ENV GIT_SSH_COMMAND='ssh -o StrictHostKeyChecking=no'

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install --force-reinstall --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Make test.sh executable
RUN chmod +x test.sh

# Command to run your test script
CMD ["./test.sh"]