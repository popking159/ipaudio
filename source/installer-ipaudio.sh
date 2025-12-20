#!/bin/bash

# Version info - UPDATE THESE for each release
version="8.09"
description="Adjust Grid list and build in EPG fetcher"
ipkurl="https://github.com/popking159/ipaudio/releases/download/IPAudio/enigma2-plugin-extensions-ipaudio_${version}_all.ipk"

echo ""
echo "IPAudio Installer v$version"
echo "================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Error: Please run as root!"
    exit 1
fi

# Test download URL first
echo "=== Testing download URL ==="
if ! wget --spider "$ipkurl" 2>/dev/null; then
    echo "ERROR: IPK not found at $ipkurl"
    echo "Check: https://github.com/popking159/ipaudio/releases"
    exit 1
fi

# CLEANUP FIRST - Remove ONLY IPAudio (preserve IPAudioPro)
echo "=== Cleaning previous IPAudio installation ==="
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/IPAudio
opkg remove enigma2-plugin-extensions-ipaudio --force-depends 2>/dev/null || true

# Backup user data
echo "=== Backing up user data ==="
backup_dir="/tmp/ipaudiobackup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"
if [ -d "/etc/enigma2/ipaudio" ]; then
    cp -r /etc/enigma2/ipaudio "$backup_dir/"
    echo "Playlists backed up to $backup_dir"
fi

# Reset IPAudio config
echo "=== Resetting IPAudio settings ==="
settings_file="/etc/enigma2/settings"
if [ -f "$settings_file" ]; then
    cp "$settings_file" "${settings_file}.backup.$(date +%Y%m%d%H%M%S)"
    sed -i '/^config.plugins.IPAudio/d' "$settings_file"
    echo "Settings reset to defaults"
fi

# Install
tmp_dir="/tmp/ipaudio-install"
mkdir -p "$tmp_dir"
cd "$tmp_dir" || exit 1

echo "=== Downloading IPAudio v$version ==="
wget -q --show-progress "$ipkurl" -O ipaudio.ipk
if [ $? -ne 0 ]; then
    echo "ERROR: Download failed!"
    rm -rf "$tmp_dir"
    exit 1
fi

echo "Download complete! ($(ls -lh ipaudio.ipk))"

# Dependencies
echo "=== Checking dependencies ==="
if ! python3 -c "import PIL" 2>/dev/null; then
    echo "Installing python3-pillow..."
    opkg update >/dev/null 2>&1
    opkg install python3-pillow
fi

# Install
echo "=== Installing IPAudio v$version ==="
if opkg list-installed | grep -q "enigma2-plugin-extensions-ipaudio"; then
    echo "Upgrading IPAudio... (IPAudioPro preserved)"
else
    echo "Fresh install... (IPAudioPro preserved)"
fi

opkg install --force-reinstall ipaudio.ipk

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "✓ Installation Successful!"
    echo "=================================="
    echo "IPAudio v$version ready!"
    echo ""
    echo "- IPAudio: CLEAN installed ✓"
    echo "- IPAudioPro: PRESERVED ✓" 
    echo "- Playlists: BACKED UP ✓"
    echo ""
    echo "=== AUTO RESTARTING GUI ==="
    sleep 3
    killall -9 enigma2
else
    echo "Installation FAILED!"
    rm -rf "$tmp_dir"
    exit 1
fi

rm -rf "$tmp_dir"
exit 0
