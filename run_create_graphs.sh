#!/bin/bash

output_dir="/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Result"
dataset="ITS4S"

# Check if the virtual environment exists
if [ ! -d "csv_virtual_env" ]; then
    echo "Virtual environment not found. Creating the environment..."
    # Create the virtual environment
    python3 -m venv csv_virtual_env
    # Activate the virtual env
    source csv_virtual_env/bin/activate
    # Install the required packages
    pip install -r requirements.txt
    # Run the script
    python3 graph_script.py "$output_dir" "$dataset"
    # Deactivate the virtual environment
    deactivate
else
    echo "Virtual environment exists. Running the script : "
    # If the environment exists, run the script without creating the environment
    source csv_virtual_env/bin/activate
    python3 graph_script.py "$output_dir" "$dataset"
    deactivate
fi
