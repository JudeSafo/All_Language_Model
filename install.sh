#!/bin/bash

# Clone the repository
git clone https://github.com/JudeSafo/All_Language_Model

# Move into the cloned repository directory
cd All_Language_Model

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

# Move the encrypted binary to appropriate location
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
