#!/bin/bash

# Check if Python is installed
if ! command -v python &> /dev/null
then
    echo "Python is not installed. Installing Python..."
    sudo apt-get update
    sudo apt-get install -y python
fi
# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "Pip is not installed. Please install it."
    exit 1
fi

# Install packages from requirements.txt
pip install -r requirements.txt

# Check the exit code of pip
if [ $? -eq 0 ]
then
    echo "Packages installed successfully."
else
    echo "Error: Failed to install packages."
fi
