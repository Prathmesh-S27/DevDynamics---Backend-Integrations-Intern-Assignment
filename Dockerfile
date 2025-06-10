FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./src ./src
COPY ./tests ./tests

# Copy the Alembic configuration
COPY alembic.ini .

# Use a startup script to handle PORT variable properly
COPY start.sh .
RUN chmod +x start.sh

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["./start.sh"]