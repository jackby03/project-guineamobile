FROM python:3.12-slim
WORKDIR /usr/src/app

# Copy requirements first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .
COPY ../src /usr/src/app/src

# Create a directory for temporary files
RUN mkdir -p /usr/src/app/tmp
VOLUME [ "/usr/src/app/tmp" ]

# Set environment variables
ENV PYTHONPATH=/usr/src/app

# Expose the application port
EXPOSE 8000

# Default command
CMD ["python", "app.py"]