FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY api/ ./api/
COPY experiments/ ./experiments/

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "api/app.py"]
