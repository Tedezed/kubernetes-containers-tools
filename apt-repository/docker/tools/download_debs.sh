#!/bin/bash

# Download DEB packages and dependencies
# By Tedezed

# Example: ./download_debs.sh nginx
# Example: ./download_debs.sh nginx 1

PACKAGE_NAME=$1
MODE=${2:-1}
DOWNLOAD_DIR=${3:-./download_apt}

# Create the specified directory to store the downloaded packages
mkdir -p "$DOWNLOAD_DIR"
cd "$DOWNLOAD_DIR"

if [ "$MODE" == "0" ]
then
    # Download the package and its dependencies
    DEPS=$(apt-cache depends $PACKAGE_NAME | grep "Depends:" | awk '{print $2}')
    for DEP in $DEPS; do
      apt-get download $DEP
      apt-get download -o Dir::Cache="$DOWNLOAD_DIR" $DEP
    done
    apt-get download -o Dir::Cache="$DOWNLOAD_DIR" $PACKAGE_NAME
else
    # Download the package and its dependencies
    apt-rdepends $PACKAGE_NAME | grep -v "^ " | grep -v "<" | while read -r pkg; do
        # Check if the package has a candidate version
        if apt-cache show $pkg &> /dev/null; then
            echo "Downloading $pkg to $DOWNLOAD_DIR..."
            apt-get download -o Dir::Cache="$DOWNLOAD_DIR" $pkg
        else
            echo "Skipping $pkg as it has no candidate."
        fi
    done
fi