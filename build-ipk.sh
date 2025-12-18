#!/bin/bash

# Configuration
PLUGIN_NAME="enigma2-plugin-extensions-ipaudio"
VERSION="8.08"
MAINTAINER="popking159"
DESCRIPTION="IPAudio - Multi-format audio streaming plugin with custom playlists"
HOMEPAGE="https://github.com/popking159/ipaudio"
SECTION="extra"
PRIORITY="optional"
ARCHITECTURE="all"
LICENSE="GPL-2.0"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$SCRIPT_DIR/build"
CONTROL_DIR="$BUILD_DIR/CONTROL"
DATA_DIR="$BUILD_DIR/usr/lib/enigma2/python/Plugins/Extensions/IPAudio"

echo ""
echo "IPAudio IPK Builder v$VERSION"
echo "================================"

# Clean previous build
rm -rf "$BUILD_DIR"
rm -f "$SCRIPT_DIR/${PLUGIN_NAME}_${VERSION}_${ARCHITECTURE}.ipk"

# Create directories
mkdir -p "$CONTROL_DIR"
mkdir -p "$DATA_DIR"
mkdir -p "$BUILD_DIR/etc/enigma2/ipaudio"

# Control file
cat > "$CONTROL_DIR/control" << EOF
Package: $PLUGIN_NAME
Version: $VERSION
Description: $DESCRIPTION
Section: $SECTION
Priority: $PRIORITY
Maintainer: $MAINTAINER
License: $LICENSE
Architecture: $ARCHITECTURE
OE: enigma2-plugin-extensions-ipaudio
Homepage: $HOMEPAGE
Depends: python3-core, python3-twisted-web, python3-pillow, python3-json, gstreamer1.0, gstreamer1.0-plugins-base, gstreamer1.0-plugins-good, gstreamer1.0-plugins-bad, gstreamer1.0-plugins-ugly, ffmpeg
Installed-Size: 0
EOF

# Scripts (postinst, prerm)
cat > "$CONTROL_DIR/postinst" << 'EOF'
#!/bin/sh
mkdir -p /etc/enigma2/ipaudio
mkdir -p /usr/lib/enigma2/python/Plugins/Extensions/IPAudio/picons/simple
mkdir -p /usr/lib/enigma2/python/Plugins/Extensions/IPAudio/picons/grid
chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/IPAudio
chmod 644 /usr/lib/enigma2/python/Plugins/Extensions/IPAudio/*.py 2>/dev/null
echo "IPAudio v8.08 installed! Restart Enigma2."
exit 0
EOF

cat > "$CONTROL_DIR/prerm" << 'EOF'
#!/bin/sh
killall -9 gst-launch-1.0 2>/dev/null
killall -9 ffmpeg 2>/dev/null
exit 0
EOF

chmod 755 "$CONTROL_DIR"/postinst "$CONTROL_DIR"/prerm

# Copy plugin files
echo "Copying plugin files..."
if [ ! -f "$SCRIPT_DIR/plugin.py" ]; then
    echo "ERROR: plugin.py not found!"
    exit 1
fi

rsync -av --exclude="*.pyc" --exclude="*.pyo" --exclude="*.sh" --exclude="*.ipk" --exclude="build-ipk.sh" "$SCRIPT_DIR/" "$DATA_DIR/"

touch "$DATA_DIR/__init__.py"

echo "Files copied: $(find "$DATA_DIR" -type f | wc -l)"

# FIXED: Create archives with FULL PATHS
echo "Creating archives..."

# 1. Data tar.gz
tar --owner=0 --group=0 -czf "$SCRIPT_DIR/data.tar.gz" -C "$BUILD_DIR" usr etc

# 2. Control tar.gz  
tar --owner=0 --group=0 -czf "$SCRIPT_DIR/control.tar.gz" -C "$CONTROL_DIR" .

# 3. debian-binary
echo "2.0" > "$SCRIPT_DIR/debian-binary"

# 4. Build IPK with FULL PATHS
PKG_NAME="${PLUGIN_NAME}_${VERSION}_${ARCHITECTURE}.ipk"
ar -r "$SCRIPT_DIR/$PKG_NAME" \
    "$SCRIPT_DIR/debian-binary" \
    "$SCRIPT_DIR/control.tar.gz" \
    "$SCRIPT_DIR/data.tar.gz"

# Update installed-size
INSTALLED_SIZE=$(du -sk "$BUILD_DIR/usr" "$BUILD_DIR/etc" 2>/dev/null | awk 'NR>1 {sum+=$1} END {print int(sum/1024)}')
sed -i "s/Installed-Size: 0/Installed-Size: $INSTALLED_SIZE/" "$CONTROL_DIR/control"

# Verify
if [ -f "$SCRIPT_DIR/$PKG_NAME" ] && ar t "$SCRIPT_DIR/$PKG_NAME" | grep -q "debian-binary"; then
    echo ""
    echo "✓ Build SUCCESSFUL!"
    echo "Package: $PKG_NAME"
    echo "Size: $(ls -lh "$SCRIPT_DIR/$PKG_NAME" | awk '{print $5}')"
    echo "Install: opkg install $PKG_NAME"
else
    echo "✗ Build FAILED!"
    rm -f "$SCRIPT_DIR/$PKG_NAME"
    exit 1
fi

# Cleanup
rm -rf "$BUILD_DIR" "$SCRIPT_DIR"/data.tar.gz "$SCRIPT_DIR"/control.tar.gz "$SCRIPT_DIR"/debian-binary
echo "Ready for GitHub!"
