# Start from a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy dependencies first (for caching layers)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the FastAPI port
EXPOSE 8080

# Start FastAPI using uvicorn. hostPort:containerPort
CMD ["uvicorn", "fastapi-main:app", "--host", "0.0.0.0", "--port", "8080"]  
