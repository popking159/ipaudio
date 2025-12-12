#!/bin/bash

# IPAudio Auto-Update Installer
# Upload this to GitHub and provide the raw URL
# wget -q --no-check-certificate https://raw.githubusercontent.com/popking159/ipaudio/main/installer-ipaudio.sh -O - | bash

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Version info (update these for each release)
version="8.1"
description="Fixed Python 3 compatibility, config corruption handling, configurable paths"
ipk_url="https://github.com/popking159/ipaudio/releases/download/IPAudio/enigma2-plugin-extensions-ipaudio_${version}_all.ipk"

# Display banner
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}  IPAudio Installer v${version}${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Error: Please run as root${NC}"
    exit 1
fi

# Function to remove ALL IPAudio config settings
reset_ipaudio_config() {
    local SETTINGS_FILE="/etc/enigma2/settings"
    
    if [ ! -f "$SETTINGS_FILE" ]; then
        return
    fi
    
    echo -e "${BLUE}Resetting IPAudio configuration...${NC}"
    
    # Check if any IPAudio config exists
    if grep -q "config.plugins.IPAudio" "$SETTINGS_FILE"; then
        # Backup settings file first
        cp "$SETTINGS_FILE" "${SETTINGS_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${YELLOW}Settings backed up${NC}"
        
        # Remove ALL IPAudio config lines
        sed -i '/^config\.plugins\.IPAudio/d' "$SETTINGS_FILE"
        
        echo -e "${GREEN}All IPAudio settings removed - will use fresh defaults${NC}"
    else
        echo -e "${GREEN}No previous IPAudio settings found${NC}"
    fi
}

# Function to backup user playlists and delays
backup_user_data() {
    echo -e "${BLUE}Checking for user data...${NC}"
    
    local BACKUP_DIR="/tmp/ipaudio_backup_$(date +%Y%m%d_%H%M%S)"
    local HAS_BACKUP=false
    
    # Backup playlists and delays (keep these!)
    if [ -d "/etc/enigma2/ipaudio" ]; then
        mkdir -p "$BACKUP_DIR"
        cp -r /etc/enigma2/ipaudio "$BACKUP_DIR/"
        echo -e "${GREEN}✓ Playlists and delays backed up to $BACKUP_DIR${NC}"
        HAS_BACKUP=true
    fi
    
    if [ "$HAS_BACKUP" = false ]; then
        echo -e "${YELLOW}No user data to backup${NC}"
    fi
}

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
    
    # Backup user playlists and delays (NOT settings)
    backup_user_data
    
    # Remove ALL config settings for clean upgrade
    reset_ipaudio_config
    
    # Remove old version
    opkg remove enigma2-plugin-extensions-ipaudio --force-depends
else
    echo -e "${YELLOW}Installing IPAudio for the first time...${NC}"
    
    # Clean any leftover config from previous installations
    reset_ipaudio_config
fi

echo -e "${YELLOW}Installing IPAudio v${version}...${NC}"
opkg install ipaudio.ipk

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}======================================${NC}"
    echo -e "${GREEN}  Installation Successful!${NC}"
    echo -e "${GREEN}======================================${NC}"
    echo -e "${GREEN}IPAudio v${version} installed${NC}"
    echo -e "${GREEN}Changes: ${description}${NC}"
    echo ""
    
    # Create settings directory if it doesn't exist
    mkdir -p /etc/enigma2/ipaudio
    
    echo -e "${BLUE}Installation summary:${NC}"
    echo -e "  ✓ Plugin installed"
    echo -e "  ✓ Settings reset to defaults"
    echo -e "  ✓ User playlists preserved (if any)"
    echo ""
    echo -e "${YELLOW}======================================${NC}"
    echo -e "${YELLOW}Important: Please restart Enigma2${NC}"
    echo -e "${YELLOW}======================================${NC}"
    echo ""
    echo -e "${BLUE}Restart options:${NC}"
    echo -e "  1. From GUI: Menu > Standby > Restart GUI"
    echo -e "  2. Command: killall -9 enigma2"
    echo ""
    
    # Ask if user wants to restart now
    read -p "Restart Enigma2 now? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}Restarting Enigma2 in 3 seconds...${NC}"
        sleep 3
        killall -9 enigma2
    else
        echo -e "${YELLOW}Please restart manually when ready${NC}"
    fi
else
    echo -e "${RED}Installation failed!${NC}"
    rm -rf "$TMP_DIR"
    exit 1
fi

# Cleanup
rm -rf "$TMP_DIR"
echo -e "${GREEN}Done!${NC}"
exit 0
