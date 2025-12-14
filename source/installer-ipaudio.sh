#!/bin/bash

# IPAudio Auto-Update Installer
# Version info (update these for each release)
version="8.04"
description="Fix wed ui to deal with all avaialble settings paths"

ipk_url="https://github.com/popking159/ipaudio/releases/download/IPAudio/enigma2-plugin-extensions-ipaudio_${version}_all.ipk"

# Display banner
echo "======================================"
echo " IPAudio Installer v${version}"
echo "======================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Error: Please run as root"
    exit 1
fi

# Function to remove ALL IPAudio config settings
reset_ipaudio_config() {
    local SETTINGS_FILE="/etc/enigma2/settings"
    if [ ! -f "$SETTINGS_FILE" ]; then
        return
    fi
    echo "Resetting IPAudio configuration..."
    # Check if any IPAudio config exists
    if grep -q "config.plugins.IPAudio" "$SETTINGS_FILE"; then
        # Backup settings file first
        cp "$SETTINGS_FILE" "${SETTINGS_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
        echo "Settings backed up"
        # Remove ALL IPAudio config lines
        sed -i '/^config\.plugins\.IPAudio/d' "$SETTINGS_FILE"
        echo "All IPAudio settings removed - will use fresh defaults"
    else
        echo "No previous IPAudio settings found"
    fi
}

# Function to backup user playlists and delays
backup_user_data() {
    echo "Checking for user data..."
    local BACKUP_DIR="/tmp/ipaudio_backup_$(date +%Y%m%d_%H%M%S)"
    local HAS_BACKUP=false
    # Backup playlists and delays (keep these!)
    if [ -d "/etc/enigma2/ipaudio" ]; then
        mkdir -p "$BACKUP_DIR"
        cp -r /etc/enigma2/ipaudio "$BACKUP_DIR/"
        echo "Playlists and delays backed up to $BACKUP_DIR"
        HAS_BACKUP=true
    fi
    if [ "$HAS_BACKUP" = false ]; then
        echo "No user data to backup"
    fi
}

# Create temp directory
TMP_DIR="/tmp/ipaudio_install"
mkdir -p "$TMP_DIR"
cd "$TMP_DIR"

echo "Downloading IPAudio v${version}..."
wget -q --show-progress "$ipk_url" -O ipaudio.ipk

if [ $? -ne 0 ]; then
    echo "Error: Download failed!"
    echo "Please check your internet connection."
    rm -rf "$TMP_DIR"
    exit 1
fi

echo "Download complete!"
echo ""

# Check if plugin is already installed
if opkg list-installed | grep -q "enigma2-plugin-extensions-ipaudio"; then
    echo "IPAudio is already installed. Upgrading..."
    # Backup user playlists and delays (NOT settings)
    backup_user_data
    # Remove ALL config settings for clean upgrade
    reset_ipaudio_config
    # Remove old version
    opkg remove enigma2-plugin-extensions-ipaudio --force-depends
else
    echo "Installing IPAudio for the first time..."
    # Clean any leftover config from previous installations
    reset_ipaudio_config
fi

echo "Checking dependencies..."
# Check for Python PIL/Pillow
if python3 -c "import PIL" 2>/dev/null; then
    echo "Python PIL/Pillow found"
else
    echo "Installing Python PIL/Pillow for picon conversion..."
    opkg update
    opkg install python3-pillow
    if [ $? -eq 0 ]; then
        echo "Python PIL/Pillow installed"
    else
        echo "Warning: Failed to install PIL/Pillow. Picon conversion will not work."
    fi
fi

echo "Installing IPAudio v${version}..."
opkg install ipaudio.ipk

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo " Installation Successful!"
    echo "======================================"
    echo "IPAudio v${version} installed"
    echo "Changes: ${description}"
    echo ""

    # Create settings directory if it doesn't exist
    mkdir -p /etc/enigma2/ipaudio
    
    echo "Installation summary:"
    echo " - Plugin installed"
    echo " - Settings reset to defaults"
    echo " - User playlists preserved (if any)"
    echo ""

    echo "======================================"
    echo " AUTO-RESTARTING ENIGMA2..."
    echo "======================================"
    echo ""
    
    # Give user 5 seconds to read before restart
    echo -n "Restarting in 5 seconds... (Ctrl+C to cancel)"
    sleep 5
    
    echo ""
    echo "Restarting Enigma2 NOW!"
    echo "Plugin will be available after restart."
    
    # SAFE Enigma2 restart sequence for all receivers
    killall -9 enigma2 >/dev/null 2>&1
    sleep 2
    /usr/bin/enigma2 >/dev/null 2>&1 &
    
    echo "Enigma2 restarted successfully!"
    echo "IPAudio plugin is now ready."
    
else
    echo "Installation failed!"
    rm -rf "$TMP_DIR"
    exit 1
fi

# Cleanup
rm -rf "$TMP_DIR"
echo "Done!"
exit 0
