# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

# Copy the shell scripts into the container
#COPY start_app.sh /usr/local/bin/

# Make the shell scripts executable
#RUN chmod +x /usr/local/bin/start_app.sh

# Copy the rest of the application code to the working directory
COPY . .

# Expose port 5000 to the outside world
EXPOSE 5000

# # Command to run the application
CMD ["flask", "run", "--reload"]
# CMD ["py", "app"]

# Run the shell script as the entry point
#ENTRYPOINT ["/usr/local/bin/start_app.sh"]  