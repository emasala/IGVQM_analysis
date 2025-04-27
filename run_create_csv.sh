#!/bin/bash

result_dir="/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Result"
mos_dir="/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Mos"
dataset="KUGVD"
use_libvmaf=True
use_essim=True

# Check if the virtual environment exists
if [ ! -d "csv_virtual_env" ]; then
    echo "Virtual environment not found. Creating the environment..."
    # Create the virtual environment
    python3 -m venv csv_virtual_env
    # Activate the virtual environment
    source csv_virtual_env/bin/activate
    # Install the required packages
    pip install -r requirements.txt
    # Run the script
    python3 analyze_results_script.py "$result_dir" "$mos_dir" "$dataset" "$use_libvmaf" "$use_essim" 
    # Deactivate the virtual environment
    deactivate
else
    echo "Virtual environment exists. Running the script : "
    # If the environment exists, run the script without creating the environment
    source csv_virtual_env/bin/activate
    python3 analyze_results_script.py "$result_dir" "$mos_dir" "$dataset" "$use_libvmaf" "$use_essim" 
    deactivate
fi
