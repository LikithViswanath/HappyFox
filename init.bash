#!/bin/bash

SCRIPT_NAME=$(basename "$0")

echo "Going inside HappyFox"
cd HappyFox || exit

echo "** Creating virtual environment (HappyFox)..."
python3 -m venv virtual-env
source virtual-env/bin/activate || { echo "Failed to activate virtualenv. Exiting..."; exit 1; }

# 2. Install requirements
echo "** Installing requirements from requirements.txt..."
pip3 install -r requirements.txt || { echo "Failed to install requirements. Exiting..."; deactivate; exit 1; }

# 3. Setup python path (assuming current directory is project root)
echo "** Setting up Python path..."
export PYTHONPATH=$PYTHONPATH:./

# 4. Start database using docker-compose
echo "** Starting database containers..."
docker-compose -f docker-compose.yaml up -d || { echo "Failed to start database containers. Exiting..."; deactivate; exit 1; }

echo "** Script ($SCRIPT_NAME) completed successfully! **"

# Deactivate virtual environment (optional)