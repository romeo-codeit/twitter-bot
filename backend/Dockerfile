# ---- Base Stage: Install dependencies ----
FROM python:3.11-slim as builder

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
# Copy only the requirements file to leverage Docker layer caching
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# ---- Final Stage: Create the production image ----
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the pre-built wheels from the builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy the application code
COPY . .

# Expose the port the app will run on
EXPOSE 5000

# The command to run the application using Gunicorn
# Using --preload is important for APScheduler to prevent multiple scheduler instances.
# The number of workers can be adjusted based on the server's resources.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--preload", "backend:create_app()"]
