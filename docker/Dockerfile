# Use official Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency files
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into container
COPY . .

# Expose the backend port
EXPOSE 8000

# Run the FastAPI app (entrypoint is backend/main.py → backend.main:app)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
