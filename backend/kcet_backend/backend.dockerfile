FROM python:3.10-slim

# -------------------------------
# Python settings
# -------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -------------------------------
# System dependencies (NO Selenium here)
# -------------------------------
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# App setup
# -------------------------------
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

# -------------------------------
# IMPORTANT:
# ❌ NO collectstatic
# ❌ NO selenium / chromium
# -------------------------------

# Actual command is controlled by docker-compose.yml
CMD ["python", "-c", "print('Backend image built successfully')"]
