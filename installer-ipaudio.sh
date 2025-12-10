#!/bin/bash
# IPAudio Auto-Update Installer
# Upload this to GitHub and provide the raw URL
# wget -q --no-check-certificate https://raw.githubusercontent.com/popking159/ipaudio/main/installer-ipaudio.sh -O - | bash

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Version info (update these for each release)
version="8.0"
description="Multi-category playlists, new skins, audio/video delay control"
ipk_url="https://github.com/popking159/ipaudio/releases/download/IPAudio/enigma2-plugin-extensions-ipaudio_${version}_all.ipk"

# Display banner
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}   IPAudio Installer v${version}${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Error: Please run as root${NC}"
    exit 1
fi

# Create temp directory
TMP_DIR="/tmp/ipaudio_install"
mkdir -p "$TMP_DIR"
cd "$TMP_DIR"

echo -e "${YELLOW}Downloading IPAudio v${version}...${NC}"
wget -q --show-progress "$ipk_url" -O ipaudio.ipk

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Download failed!${NC}"
    echo -e "${RED}Please check your internet connection.${NC}"
    rm -rf "$TMP_DIR"
    exit 1
fi

echo -e "${GREEN}Download complete!${NC}"
echo ""

# Check if plugin is already installed
if opkg list-installed | grep -q "enigma2-plugin-extensions-ipaudio"; then
    echo -e "${YELLOW}IPAudio is already installed. Upgrading...${NC}"
    opkg remove enigma2-plugin-extensions-ipaudio --force-depends
fi

echo -e "${YELLOW}Installing IPAudio v${version}...${NC}"
opkg install ipaudio.ipk

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}======================================${NC}"
    echo -e "${GREEN}   Installation Successful!${NC}"
    echo -e "${GREEN}======================================${NC}"
    echo -e "${GREEN}IPAudio v${version} installed${NC}"
    echo -e "${GREEN}Changes: ${description}${NC}"
    echo ""
    echo -e "${YELLOW}Please restart Enigma2 to use the plugin${NC}"
else
    echo -e "${RED}Installation failed!${NC}"
    rm -rf "$TMP_DIR"
    exit 1
fi

# Cleanup
rm -rf "$TMP_DIR"
exit 0
