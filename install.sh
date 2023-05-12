#!/bin/bash

# Check if script is being run from within the repository folder
if [[ $(basename "$PWD") == "All_Language_Model" ]]; then
    REPO_FOLDER="$PWD"
else
    # Clone the repository
    git clone https://github.com/JudeSafo/All_Language_Model
    REPO_FOLDER="$PWD/All_Language_Model"
    cd "$REPO_FOLDER"
fi

# Move into the repository directory
cd "$REPO_FOLDER"

# Install shc if not already installed
if ! command -v shc >/dev/null 2>&1; then
    echo "shc is not installed. Installing shc..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install shc
    else
        # Assuming Linux distribution with package manager
        sudo apt-get update
        sudo apt-get install -y shc
    fi
else
    echo "shc is already installed."
fi

# Encrypt the shell script using shc
shc -f ecocrumb.sh

# Move the encrypted binary to the appropriate location
if [[ "$OSTYPE" == "darwin"* ]]; then
    sudo mv ecocrumb.sh.x /usr/local/bin/ecocrumb
    sudo mv ecocrumb.1 /usr/local/share/man/man1/
else
    sudo mv ecocrumb.sh.x /usr/bin/ecocrumb
    sudo mv ecocrumb.1 /usr/share/man/man1/
fi

# Generate the man page database
sudo mandb

echo "Installation completed successfully."
