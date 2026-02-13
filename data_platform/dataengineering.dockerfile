# ------------------------------------
# Spark + Java base image
# ------------------------------------
FROM apache/spark:3.4.2

# ------------------------------------
# Switch to root for installs
# ------------------------------------
USER root

# ------------------------------------
# Set working directory
# ------------------------------------
WORKDIR /opt/spark/app

# ------------------------------------
# Copy requirements
# ------------------------------------
COPY requirements.txt .

# ------------------------------------
# Install Python dependencies
# ------------------------------------
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------------------
# Copy data platform code
# ------------------------------------
COPY data_platform/ data_platform/

# ------------------------------------
# Default shell
# ------------------------------------
CMD ["bash"]
