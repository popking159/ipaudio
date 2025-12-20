#!/bin/bash

# IPAudio Installer - Clean upgrade path
version="8.09"
ipkurl="https://github.com/popking159/ipaudio/releases/download/IPAudio/enigma2-plugin-extensions-ipaudio_${version}_all.ipk"

echo ""
echo "IPAudio Installer v$version"
echo "============================"

# Check root
if [ "$EUID" -ne 0 ]; then
    echo "Error: Please run as root!"
    exit 1
fi

# Test URL
echo "=== Testing download ==="
if ! wget --spider "$ipkurl" 2>/dev/null; then
    echo "ERROR: IPK not found! Check GitHub releases"
    exit 1
fi

# CHECK & REMOVE PREVIOUS IPAudio ONLY
echo "=== Checking for previous IPAudio ==="
if opkg list-installed | grep -q "enigma2-plugin-extensions-ipaudio"; then
    echo "Previous IPAudio found - removing..."
    opkg remove enigma2-plugin-extensions-ipaudio --force-depends
    rm -rf /usr/lib/enigma2/python/Plugins/Extensions/IPAudio
    echo "✓ IPAudio removed"
else
    echo "No previous IPAudio - fresh install"
fi

# Backup playlists ONLY if exist
echo "=== Backing up playlists ==="
if [ -d "/etc/enigma2/ipaudio" ] && [ "$(ls -A /etc/enigma2/ipaudio/*.json 2>/dev/null | wc -l)" -gt 0 ]; then
    backup_dir="/tmp/ipaudiobackup-$(date +%Y%m%d-%H%M%S)"
    cp -r /etc/enigma2/ipaudio "$backup_dir/"
    echo "✓ Playlists backed up: $backup_dir"
fi

# Download & Install
tmp_dir="/tmp/ipaudio-install"
mkdir -p "$tmp_dir"
cd "$tmp_dir" || exit 1

echo "=== Downloading v$version ==="
wget -q --show-progress "$ipkurl" -O ipaudio.ipk || { echo "Download failed!"; rm -rf "$tmp_dir"; exit 1; }

echo "=== Installing ==="
opkg install ./ipaudio.ipk

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 IPAudio v$version INSTALLED SUCCESSFULLY!"
    echo "====================================="
    echo "- Plugin: /usr/lib/enigma2/python/Plugins/Extensions/IPAudio/"
    echo "- Playlists: /etc/enigma2/ipaudio/"
    echo ""
    echo "🔄 RESTARTING ENIGMA2 in 3s..."
    sleep 3
    killall -9 enigma2
else
    echo "❌ Installation FAILED!"
    rm -rf "$tmp_dir"
    exit 1
fi

rm -rf "$tmp_dir"
exit 0
