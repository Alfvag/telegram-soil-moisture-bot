FROM python:3.11-slim

# Install required system dependencies including MySQL ODBC driver
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    gnupg \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Add MySQL ODBC repository and install driver
RUN wget https://dev.mysql.com/get/mysql-apt-config_0.8.29-1_all.deb \
    && dpkg -i mysql-apt-config_0.8.29-1_all.deb \
    && apt-get update \
    && apt-get install -y mysql-connector-odbc \
    && rm mysql-apt-config_0.8.29-1_all.deb

# Install matplotlib dependencies
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py bot_helpers.py db_helpers.py .env ./

# Run the bot
CMD ["python", "app.py"]