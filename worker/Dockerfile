FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for NetCDF / scientific libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libhdf5-dev \
    libnetcdf-dev \
    && rm -rf /var/lib/apt/lists/*

# Install worker dependencies
COPY worker/requirements.txt ./worker/requirements.txt
RUN pip install --no-cache-dir -r worker/requirements.txt

# Install LDAR-Sim simulation dependencies
COPY LDAR_Sim/install/requirements.txt ./ldar_sim_requirements.txt
RUN pip install --no-cache-dir -r ldar_sim_requirements.txt || true

# Copy the entire LDAR-Sim package (simulation code stays untouched)
COPY LDAR_Sim/ ./LDAR_Sim/

# Copy worker source
COPY worker/ ./worker/

# Set Python path so ldar_sim_main.py can find its modules
ENV PYTHONPATH=/app/LDAR_Sim/src:/app/LDAR_Sim/external_sensors

WORKDIR /app/worker

CMD ["python", "worker_main.py"]
