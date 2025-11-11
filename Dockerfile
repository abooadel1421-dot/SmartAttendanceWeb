# Use an official Python runtime as a parent image  
FROM python:3.9-slim-buster  

# Set the working directory in the container  
WORKDIR /app  

# Install any needed packages specified in requirements.txt  
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the rest of the application code to the container  
COPY . .  

# Set environment variables (if needed)  
# ENV FLASK_APP=wsgi.py  
# ENV FLASK_ENV=production  

# Expose the port Flask runs on  
EXPOSE 5000  

# Run the application using Gunicorn (or Flask's built-in server for development)  
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]  
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]