# Install base image
FROM python:3.7-slim-buster

# Install required dependencies
RUN pip install Flask
RUN pip install pymongo

# Copy the source code in the directory to the container
# Store it in a folder called /app.
Add . /app

# Set working directory to /app so we can execute command in it
WORKDIR /app

# Declare environment variables
ENV FLASK_app=app.python
ENV FLASK_ENV=development

# Expose the port that Flask is running on 
EXPOSE 5000

# Run Flask
CMD ["flask", "run", "--host=0.0.0.0"]
