# Use a stable Python version (3.11 recommended for compatibility)
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies for lxml and newspaper3k
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement files first (for caching)
COPY requirements.txt .

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Render will use
EXPOSE 10000

# Run the application
CMD ["uvicorn", "blogsummarizer:app", "--host", "0.0.0.0", "--port", "10000"]
