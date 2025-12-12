#!/bin/bash

# IPAudio IPK Builder Script
# This script creates an installable IPK package for Enigma2

# Configuration
PLUGIN_NAME="enigma2-plugin-extensions-ipaudio"
VERSION="8.03"
MAINTAINER="popking159"
DESCRIPTION="IPAudio - Multi-format audio streaming plugin with custom playlists"
HOMEPAGE="https://github.com/popking159/ipaudio"
SECTION="extra"
PRIORITY="optional"
ARCHITECTURE="all"
LICENSE="GPL-2.0"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Script directory: ${SCRIPT_DIR}"

# Paths
BUILD_DIR="${SCRIPT_DIR}/build"
CONTROL_DIR="${BUILD_DIR}/CONTROL"
DATA_DIR="${BUILD_DIR}/usr/lib/enigma2/python/Plugins/Extensions/IPAudio"

echo "======================================"
echo " IPAudio IPK Builder v${VERSION}"
echo "======================================"
echo ""

# Clean previous build
echo "Cleaning previous build..."
rm -rf ${BUILD_DIR}
rm -f ${SCRIPT_DIR}/${PLUGIN_NAME}_${VERSION}_${ARCHITECTURE}.ipk

# Create directory structure
echo "Creating directory structure..."
mkdir -p ${CONTROL_DIR}
mkdir -p ${DATA_DIR}
mkdir -p ${BUILD_DIR}/etc/enigma2/ipaudio

# Create control file
echo "Creating control file..."
cat > ${CONTROL_DIR}/control << EOF
Package: ${PLUGIN_NAME}
Version: ${VERSION}
Description: ${DESCRIPTION}
 IPAudio is a powerful audio streaming plugin for Enigma2 with support for:
 - Multiple audio format streaming (GStreamer, FFmpeg)
 - Custom multi-category playlists (Sport, Quran, Music, etc.)
 - Web interface for playlist management with drag-and-drop
 - Three color themes: Orange, Teal, Lime
 - Grid and List view modes
 - Audio/Video delay synchronization (0.5s increments)
 - TimeShift delay control for live TV
 - Network status monitoring
 - Automatic updates from GitHub
 - Picon support for channels (simple & grid sizes)
 - Built-in picon converter
Section: ${SECTION}
Priority: ${PRIORITY}
Maintainer: ${MAINTAINER}
License: ${LICENSE}
Architecture: ${ARCHITECTURE}
OE: enigma2-plugin-extensions-ipaudio
Homepage: ${HOMEPAGE}
Depends: python3-core, python3-twisted-web, python3-pillow, python3-json, gstreamer1.0, gstreamer1.0-plugins-base, gstreamer1.0-plugins-good, gstreamer1.0-plugins-bad, gstreamer1.0-plugins-ugly, ffmpeg
Recommends: python3-requests, python3-six
Source: https://github.com/popking159/ipaudio
EOF

# Create postinst script (run after installation)
echo "Creating postinst script..."
cat > ${CONTROL_DIR}/postinst << 'EOF'
#!/bin/sh
echo "Configuring IPAudio..."

# Create directory for playlists
mkdir -p /etc/enigma2/ipaudio

# Create picon directories
mkdir -p /usr/lib/enigma2/python/Plugins/Extensions/IPAudio/picons/simple
mkdir -p /usr/lib/enigma2/python/Plugins/Extensions/IPAudio/picons/grid

# Set permissions
chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/IPAudio
chmod 644 /usr/lib/enigma2/python/Plugins/Extensions/IPAudio/*.py 2>/dev/null
chmod 755 /etc/enigma2/ipaudio

echo ""
echo "=================================="
echo " IPAudio installed successfully!"
echo "=================================="
echo ""
echo "Please restart Enigma2 to activate the plugin"
echo "Access web interface at: http://box-ip:8080/ipaudio"
echo ""
exit 0
EOF

# Create prerm script (run before removal)
echo "Creating prerm script..."
cat > ${CONTROL_DIR}/prerm << 'EOF'
#!/bin/sh
echo "Removing IPAudio..."

# Stop all IPAudio processes
killall -9 gst-launch-1.0 2>/dev/null
killall -9 ffmpeg 2>/dev/null

# Backup playlists before removal
if [ -d /etc/enigma2/ipaudio ]; then
    echo "Backing up playlists..."
    tar czf /tmp/ipaudio_playlists_backup.tar.gz /etc/enigma2/ipaudio 2>/dev/null
fi
exit 0
EOF

# Make scripts executable
chmod 755 ${CONTROL_DIR}/postinst
chmod 755 ${CONTROL_DIR}/prerm

# Copy ALL plugin files (excluding .pyc and .sh)
echo "Copying plugin files..."

if [ ! -f "${SCRIPT_DIR}/plugin.py" ]; then
    echo "Error: plugin.py not found in ${SCRIPT_DIR}!"
    exit 1
fi

# Use find to copy all files except .pyc and .sh
echo "Copying all plugin files (excluding .pyc and .sh)..."
find "${SCRIPT_DIR}" -maxdepth 1 -type f \
    ! -name "*.pyc" \
    ! -name "*.sh" \
    ! -name "*.ipk" \
    ! -name "*.tar.gz" \
    -exec cp {} "${DATA_DIR}/" \;

# Copy picons directory if exists
if [ -d "${SCRIPT_DIR}/picons" ]; then
    echo "Copying picons directory..."
    cp -r "${SCRIPT_DIR}/picons" "${DATA_DIR}/"
    # Remove .pyc files from picons
    find "${DATA_DIR}/picons" -name "*.pyc" -delete
fi

# Create __init__.py if it doesn't exist
if [ ! -f "${DATA_DIR}/__init__.py" ]; then
    echo "Creating __init__.py..."
    cat > ${DATA_DIR}/__init__.py << 'EOF'
#!/usr/bin/python
# -*- coding: utf-8 -*-
EOF
fi

# Count files
FILE_COUNT=$(find "${DATA_DIR}" -type f | wc -l)
echo "Copied ${FILE_COUNT} files to package"

# List what was copied
echo ""
echo "Files included in package:"
find "${DATA_DIR}" -type f -exec basename {} \; | sort

# Create default config files
echo ""
echo "Creating default configuration..."
cat > ${BUILD_DIR}/etc/enigma2/ipaudio/ipaudio_sport.json << 'EOF'
{
  "playlist": []
}
EOF

cat > ${BUILD_DIR}/etc/enigma2/ipaudio/ipaudio_quran.json << 'EOF'
{
  "playlist": []
}
EOF

# Create conffiles
echo "Creating conffiles list..."
cat > ${CONTROL_DIR}/conffiles << EOF
/etc/enigma2/ipaudio/ipaudio_sport.json
/etc/enigma2/ipaudio/ipaudio_quran.json
EOF

# Calculate installed size
echo "Calculating package size..."
INSTALLED_SIZE=$(du -sk ${BUILD_DIR}/usr ${BUILD_DIR}/etc 2>/dev/null | awk '{sum+=$1} END {print sum}')
echo "Installed-Size: ${INSTALLED_SIZE}" >> ${CONTROL_DIR}/control

# Create data tarball
echo "Creating data archive..."
cd ${BUILD_DIR}
tar czf ${SCRIPT_DIR}/data.tar.gz ./usr ./etc
cd ${SCRIPT_DIR}

# Create control tarball
echo "Creating control archive..."
cd ${CONTROL_DIR}
tar czf ${SCRIPT_DIR}/control.tar.gz ./*
cd ${SCRIPT_DIR}

# Create debian-binary
echo "Creating debian-binary..."
echo "2.0" > ${SCRIPT_DIR}/debian-binary

# Create IPK package
echo "Building IPK package..."
PKG_NAME="${PLUGIN_NAME}_${VERSION}_${ARCHITECTURE}.ipk"
cd ${SCRIPT_DIR}
ar -r ${PKG_NAME} debian-binary control.tar.gz data.tar.gz

# Cleanup temporary files
echo "Cleaning up..."
rm -rf ${BUILD_DIR}
rm -f ${SCRIPT_DIR}/debian-binary
rm -f ${SCRIPT_DIR}/control.tar.gz
rm -f ${SCRIPT_DIR}/data.tar.gz

# Display results
if [ -f ${SCRIPT_DIR}/${PKG_NAME} ]; then
    PKG_SIZE=$(ls -lh ${SCRIPT_DIR}/${PKG_NAME} | awk '{print $5}')
    echo ""
    echo "======================================"
    echo " Build Successful!"
    echo "======================================"
    echo "Package: ${PKG_NAME}"
    echo "Size: ${PKG_SIZE}"
    echo "Version: ${VERSION}"
    echo "Location: ${SCRIPT_DIR}/${PKG_NAME}"
    echo ""
    echo "Install with:"
    echo "opkg install ${PKG_NAME}"
    echo ""
else
    echo "Build failed!"
    exit 1
fi
