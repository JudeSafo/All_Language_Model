#!/bin/bash

# Check if script is being run directly or through curl
if [ -z "$INSTALL_SCRIPT" ]; then
  # Set the installation script URL
  INSTALL_SCRIPT="https://raw.githubusercontent.com/JudeSafo/All_Language_Model/main/install.sh"

  # Download the installation script
  if ! command -v curl >/dev/null 2>&1; then
    echo "curl is not installed. Please install curl and try again."
    exit 1
  fi

  curl -o install.sh -sSfL "$INSTALL_SCRIPT" || { echo "Failed to download the installation script."; exit 1; }

  # Execute the downloaded installation script
  bash install.sh

  # Clean up the downloaded script
  rm install.sh

  exit 0
fi

# Move into the cloned repository directory
cd "$(dirname "$0")"

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
