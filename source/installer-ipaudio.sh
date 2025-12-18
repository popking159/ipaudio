#!/bin/bash

# Version info - UPDATE THESE for each release
version="8.08"
description="Adjust Grid list and build in EPG fetcher"
ipkurl="https://github.com/popking159/ipaudio/releases/download/IPAudio/enigma2-plugin-extensions-ipaudio-v${version}-all.ipk"

echo ""
echo "IPAudio Installer v$version"
echo "================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Error: Please run as root!"
    exit 1
fi

# CLEANUP FIRST - Remove ONLY IPAudio (preserve IPAudioPro)
echo "=== Cleaning previous IPAudio installation ==="
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/IPAudio
opkg remove enigma2-plugin-extensions-ipaudio --force-depends 2>/dev/null || true

# Backup user data (playlists/delays)
echo "=== Backing up user data ==="
backup_dir="/tmp/ipaudiobackup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"
if [ -d "/etc/enigma2/ipaudio" ]; then
    cp -r /etc/enigma2/ipaudio "$backup_dir/" 2>/dev/null || true
    echo "Playlists backed up to $backup_dir"
fi

# Reset ALL IPAudio config settings for clean install
echo "=== Resetting IPAudio settings ==="
settings_file="/etc/enigma2/settings"
if [ -f "$settings_file" ]; then
    cp "$settings_file" "${settings_file}.backup.$(date +%Y%m%d%H%M%S)"
    sed -i '/^config.plugins.IPAudio/d' "$settings_file"
    echo "Settings reset - fresh defaults will be used"
fi

# Create temp directory
tmp_dir="/tmp/ipaudio-install"
mkdir -p "$tmp_dir"
cd "$tmp_dir" || exit 1

echo "=== Downloading IPAudio v$version ==="
wget -q --show-progress "$ipkurl" -O ipaudio.ipk
if [ $? -ne 0 ]; then
    echo "Error: Download failed!"
    echo "Please check your internet connection."
    rm -rf "$tmp_dir"
    exit 1
fi

echo "Download complete!"

# Check/install dependencies
echo "=== Checking dependencies ==="
if ! python3 -c "import PIL" 2>/dev/null; then
    echo "Installing Python PIL/Pillow for picon conversion..."
    opkg update
    opkg install python3-pillow
fi

# Install/Upgrade
echo "=== Installing IPAudio v$version ==="
if opkg list-installed | grep -q "enigma2-plugin-extensions-ipaudio"; then
    echo "Upgrading existing IPAudio... (IPAudioPro preserved)"
else
    echo "Fresh IPAudio installation... (IPAudioPro preserved)"
fi

opkg install --force-reinstall ipaudio.ipk

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "Installation Successful!"
    echo "=================================="
    echo "IPAudio v$version installed"
    echo "$description"
    echo ""
    echo "Installation summary:"
    echo "- IPAudio: CLEAN installed"
    echo "- IPAudioPro: PRESERVED ✓"
    echo "- Settings: Reset to defaults"
    echo "- Playlists: Preserved in $backup_dir"
    echo ""
    
    # AUTO RESTART GUI
    echo "=== Restarting Enigma2 GUI (5 seconds) ==="
    sleep 5
    killall -9 enigma2
    echo "GUI restarted! Plugin ready."
else
    echo "Installation failed!"
    rm -rf "$tmp_dir"
    exit 1
fi

rm -rf "$tmp_dir"
exit 0
