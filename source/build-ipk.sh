#!/bin/bash
# IPAudio IPK Builder Script
# This script creates an installable IPK package for Enigma2

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PLUGIN_NAME="enigma2-plugin-extensions-ipaudio"
VERSION="8.02"
MAINTAINER="popking159"
DESCRIPTION="IPAudio - Multi-format audio streaming plugin with custom playlists"
HOMEPAGE="https://github.com/popking159/ipaudio"
SECTION="extra"
PRIORITY="optional"
ARCHITECTURE="all"
LICENSE="GPL-2.0"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "${BLUE}Script directory: ${SCRIPT_DIR}${NC}"

# Paths
BUILD_DIR="${SCRIPT_DIR}/build"
CONTROL_DIR="${BUILD_DIR}/CONTROL"
DATA_DIR="${BUILD_DIR}/usr/lib/enigma2/python/Plugins/Extensions/IPAudio"

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}   IPAudio IPK Builder v${VERSION}${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Clean previous build
echo -e "${YELLOW}Cleaning previous build...${NC}"
rm -rf ${BUILD_DIR}
rm -f ${SCRIPT_DIR}/${PLUGIN_NAME}_${VERSION}_${ARCHITECTURE}.ipk

# Create directory structure
echo -e "${YELLOW}Creating directory structure...${NC}"
mkdir -p ${CONTROL_DIR}
mkdir -p ${DATA_DIR}
mkdir -p ${BUILD_DIR}/etc/enigma2/ipaudio

# Create control file
echo -e "${YELLOW}Creating control file...${NC}"
cat > ${CONTROL_DIR}/control << EOF
Package: ${PLUGIN_NAME}
Version: ${VERSION}
Description: ${DESCRIPTION}
 IPAudio is a powerful audio streaming plugin for Enigma2 with support for:
 - Multiple audio format streaming (GStreamer, FFmpeg)
 - Custom multi-category playlists (Sport, Quran, Music, etc.)
 - Web interface for playlist management with drag-and-drop
 - Three color themes: Orange, Teal, Lime
 - Audio/Video delay synchronization (0.5s increments)
 - TimeShift delay control for live TV
 - Network status monitoring
 - Automatic updates from GitHub
 - Picon support for channels
Section: ${SECTION}
Priority: ${PRIORITY}
Maintainer: ${MAINTAINER}
License: ${LICENSE}
Architecture: ${ARCHITECTURE}
OE: enigma2-plugin-extensions-ipaudio
Homepage: ${HOMEPAGE}
Depends: python3-core, python3-twisted-web, python3-json, gstreamer1.0, gstreamer1.0-plugins-base, gstreamer1.0-plugins-good, gstreamer1.0-plugins-bad, gstreamer1.0-plugins-ugly, ffmpeg
Recommends: python3-requests, python3-six
Source: https://github.com/popking159/ipaudio
EOF

# Create preinst script (run before installation)
echo -e "${YELLOW}Creating preinst script...${NC}"
cat > ${CONTROL_DIR}/preinst << 'EOF'
#!/bin/sh
# Pre-installation script

echo "Preparing IPAudio installation..."

# Backup existing config if present
if [ -f /etc/enigma2/ipaudio.json ]; then
    echo "Backing up existing playlist..."
    cp /etc/enigma2/ipaudio.json /tmp/ipaudio_backup.json
fi

# Stop any running IPAudio processes
killall -9 gst-launch-1.0 2>/dev/null
killall -9 ffmpeg 2>/dev/null

exit 0
EOF

# Create postinst script (run after installation)
echo -e "${YELLOW}Creating postinst script...${NC}"
cat > ${CONTROL_DIR}/postinst << 'EOF'
#!/bin/sh
# Post-installation script

echo "Configuring IPAudio..."

# Create directory for playlists
mkdir -p /etc/enigma2/ipaudio

# Create directory for picons
mkdir -p /usr/lib/enigma2/python/Plugins/Extensions/IPAudio/picons

# Restore backup if exists
if [ -f /tmp/ipaudio_backup.json ]; then
    echo "Restoring playlist backup..."
    cp /tmp/ipaudio_backup.json /etc/enigma2/ipaudio.json
    rm /tmp/ipaudio_backup.json
fi

# Set permissions
chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/IPAudio
chmod 644 /usr/lib/enigma2/python/Plugins/Extensions/IPAudio/*.py
chmod 644 /usr/lib/enigma2/python/Plugins/Extensions/IPAudio/*.pyo 2>/dev/null
chmod 755 /etc/enigma2/ipaudio

# Create default empty playlists if they don't exist
if [ ! -f /etc/enigma2/ipaudio/ipaudio_sport.json ]; then
    echo '{"playlist": []}' > /etc/enigma2/ipaudio/ipaudio_sport.json
fi

if [ ! -f /etc/enigma2/ipaudio/ipaudio_quran.json ]; then
    echo '{"playlist": []}' > /etc/enigma2/ipaudio/ipaudio_quran.json
fi

echo ""
echo "=================================="
echo "  IPAudio installed successfully!"
echo "=================================="
echo ""
echo "Please restart Enigma2 to activate the plugin"
echo "Access web interface at: http://box-ip:8080/ipaudio"
echo ""

exit 0
EOF

# Create prerm script (run before removal)
echo -e "${YELLOW}Creating prerm script...${NC}"
cat > ${CONTROL_DIR}/prerm << 'EOF'
#!/bin/sh
# Pre-removal script

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

# Create postrm script (run after removal)
echo -e "${YELLOW}Creating postrm script...${NC}"
cat > ${CONTROL_DIR}/postrm << 'EOF'
#!/bin/sh
# Post-removal script

echo "IPAudio removed"
echo "Playlist backup saved to: /tmp/ipaudio_playlists_backup.tar.gz"

exit 0
EOF

# Make scripts executable
chmod 755 ${CONTROL_DIR}/preinst
chmod 755 ${CONTROL_DIR}/postinst
chmod 755 ${CONTROL_DIR}/prerm
chmod 755 ${CONTROL_DIR}/postrm

# Copy plugin files
echo -e "${YELLOW}Copying plugin files...${NC}"

# Check if source files exist in script directory
if [ ! -f "${SCRIPT_DIR}/plugin.py" ]; then
    echo -e "${RED}Error: plugin.py not found in ${SCRIPT_DIR}!${NC}"
    echo -e "${RED}Please ensure all plugin files are in the same directory as this script${NC}"
    echo ""
    echo -e "${YELLOW}Required files:${NC}"
    echo "  - plugin.py"
    echo "  - skin.py"
    echo "  - Console2.py"
    echo "  - keymap.xml"
    echo "  - hosts.json"
    echo "  - version"
    echo "  - __init__.py (optional)"
    echo "  - logo.png (optional)"
	echo "  - default_picon.png (optional)"
    exit 1
fi

cp ${SCRIPT_DIR}/plugin.py ${DATA_DIR}/
cp ${SCRIPT_DIR}/skin.py ${DATA_DIR}/

# Copy optional __init__.py or create it
if [ -f "${SCRIPT_DIR}/__init__.py" ]; then
    cp ${SCRIPT_DIR}/__init__.py ${DATA_DIR}/
else
    echo "#!/usr/bin/python" > ${DATA_DIR}/__init__.py
    echo "# -*- coding: utf-8 -*-" >> ${DATA_DIR}/__init__.py
fi

cp ${SCRIPT_DIR}/Console2.py ${DATA_DIR}/
cp ${SCRIPT_DIR}/keymap.xml ${DATA_DIR}/
cp ${SCRIPT_DIR}/hosts.json ${DATA_DIR}/
cp ${SCRIPT_DIR}/version ${DATA_DIR}/

# Copy logo if exists
if [ -f "${SCRIPT_DIR}/logo.png" ]; then
    cp ${SCRIPT_DIR}/logo.png ${DATA_DIR}/
else
    echo -e "${YELLOW}Warning: logo.ong not found (optional)${NC}"
fi
# Copy default_picon if exists
if [ -f "${SCRIPT_DIR}/default_picon.png" ]; then
    cp ${SCRIPT_DIR}/default_picon.png ${DATA_DIR}/
else
    echo -e "${YELLOW}Warning: default_picon.ong not found (optional)${NC}"
fi
# Copy webif.py if exists
if [ -f "${SCRIPT_DIR}/webif.py" ]; then
    cp ${SCRIPT_DIR}/webif.py ${DATA_DIR}/
    echo -e "${GREEN}Web interface included${NC}"
fi

# Create default config files
echo -e "${YELLOW}Creating default configuration...${NC}"
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

# Create conffiles (files that should be preserved on upgrade)
echo -e "${YELLOW}Creating conffiles list...${NC}"
cat > ${CONTROL_DIR}/conffiles << EOF
/etc/enigma2/ipaudio/ipaudio_sport.json
/etc/enigma2/ipaudio/ipaudio_quran.json
EOF

# Calculate installed size
echo -e "${YELLOW}Calculating package size...${NC}"
INSTALLED_SIZE=$(du -sk ${BUILD_DIR}/usr ${BUILD_DIR}/etc 2>/dev/null | awk '{sum+=$1} END {print sum}')
echo "Installed-Size: ${INSTALLED_SIZE}" >> ${CONTROL_DIR}/control

# Create data tarball
echo -e "${YELLOW}Creating data archive...${NC}"
cd ${BUILD_DIR}
tar czf ${SCRIPT_DIR}/data.tar.gz ./usr ./etc
cd ${SCRIPT_DIR}

# Create control tarball
echo -e "${YELLOW}Creating control archive...${NC}"
cd ${CONTROL_DIR}
tar czf ${SCRIPT_DIR}/control.tar.gz ./*
cd ${SCRIPT_DIR}

# Create debian-binary
echo -e "${YELLOW}Creating debian-binary...${NC}"
echo "2.0" > ${SCRIPT_DIR}/debian-binary

# Create IPK package
echo -e "${YELLOW}Building IPK package...${NC}"
PKG_NAME="${PLUGIN_NAME}_${VERSION}_${ARCHITECTURE}.ipk"
cd ${SCRIPT_DIR}
ar -r ${PKG_NAME} debian-binary control.tar.gz data.tar.gz

# Cleanup temporary files
echo -e "${YELLOW}Cleaning up...${NC}"
rm -rf ${BUILD_DIR}
rm -f ${SCRIPT_DIR}/debian-binary
rm -f ${SCRIPT_DIR}/control.tar.gz
rm -f ${SCRIPT_DIR}/data.tar.gz

# Display results
if [ -f ${SCRIPT_DIR}/${PKG_NAME} ]; then
    PKG_SIZE=$(ls -lh ${SCRIPT_DIR}/${PKG_NAME} | awk '{print $5}')
    echo ""
    echo -e "${GREEN}======================================${NC}"
    echo -e "${GREEN}   Build Successful!${NC}"
    echo -e "${GREEN}======================================${NC}"
    echo -e "${GREEN}Package: ${PKG_NAME}${NC}"
    echo -e "${GREEN}Size: ${PKG_SIZE}${NC}"
    echo -e "${GREEN}Version: ${VERSION}${NC}"
    echo -e "${GREEN}Location: ${SCRIPT_DIR}/${PKG_NAME}${NC}"
    echo ""
    echo -e "${YELLOW}Install with:${NC}"
    echo -e "${BLUE}opkg install ${SCRIPT_DIR}/${PKG_NAME}${NC}"
    echo ""
    echo -e "${YELLOW}Or upload to box and install:${NC}"
    echo -e "${BLUE}scp ${SCRIPT_DIR}/${PKG_NAME} root@box-ip:/tmp/${NC}"
    echo -e "${BLUE}ssh root@box-ip 'opkg install /tmp/${PKG_NAME}'${NC}"
    echo ""
else
    echo -e "${RED}Build failed!${NC}"
    exit 1
fi
