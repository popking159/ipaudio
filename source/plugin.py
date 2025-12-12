from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.Button import Button
from Screens.MessageBox import MessageBox
from Components.MenuList import MenuList
from Tools.BoundFunction import boundFunction
from GlobalActions import globalActionMap
try:
    from keymapparser import readKeymap
except:
    from Components.ActionMap import loadKeymap as readKeymap
from Components.Sources.StaticText import StaticText
from Components.config import (
    config, ConfigSelectionNumber, getConfigListEntry, ConfigSelection, 
    ConfigYesNo, ConfigInteger, ConfigSubsection, ConfigText, configfile, 
    NoSave
)
from Components.ConfigList import ConfigListScreen
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from enigma import eConsoleAppContainer, getDesktop, eListboxPythonMultiContent, gFont, RT_HALIGN_LEFT, RT_VALIGN_CENTER, RT_WRAP
from enigma import iPlayableService, eTimer, loadPNG
from Components.ServiceEventTracker import ServiceEventTracker
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Tools.Directories import fileExists
try:
    from enigma import eAlsaOutput
    HAVE_EALSA = True
except ImportError:
    HAVE_EALSA = False
from Plugins.Extensions.IPAudio.Console2 import Console2
import os
import json
import subprocess
import signal
from datetime import datetime
from .skin import *
from sys import version_info
from collections import OrderedDict

PY3 = version_info[0] == 3
# ADD THIS LINE - Define maximum delay
MAXDELAY = 200

config.plugins.IPAudio = ConfigSubsection()
config.plugins.IPAudio.currentService = ConfigText()
config.plugins.IPAudio.player = ConfigSelection(default="gst1.0-ipaudio", choices=[
                ("gst1.0-ipaudio", _("Gstreamer")),
                ("ff-ipaudio", _("FFmpeg")),
            ])
config.plugins.IPAudio.sync = ConfigSelection(default="alsasink", choices=[
                ("alsasink", _("alsasink")),
                ("osssink", _("osssink")),
                ("autoaudiosink", _("autoaudiosink")),
            ])
config.plugins.IPAudio.skin = ConfigSelection(default="orange", choices=[
    ("orange", _("Orange")),
    ("teal", _("Teal")),
    ("lime", _("Lime"))
])
config.plugins.IPAudio.update = ConfigYesNo(default=True)
config.plugins.IPAudio.mainmenu = ConfigYesNo(default=False)
config.plugins.IPAudio.keepaudio = ConfigYesNo(default=False)
config.plugins.IPAudio.volLevel = ConfigSelectionNumber(default=1, stepwidth=1, min=1, max=100, wraparound=True)
config.plugins.IPAudio.audioDelay = ConfigInteger(default=0, limits=(-10, 60))  # -10s to 60s
config.plugins.IPAudio.tsDelay = ConfigInteger(default=5, limits=(0, 300))  # 0s to 300s (5 minutes)
config.plugins.IPAudio.delay = NoSave(ConfigInteger(default=5, limits=(0, 300)))
config.plugins.IPAudio.playlist = ConfigSelection(choices=[("1", _("Press OK"))], default="1")
config.plugins.IPAudio.running = ConfigYesNo(default=False)
config.plugins.IPAudio.lastidx = ConfigText()
config.plugins.IPAudio.lastplayed = NoSave(ConfigText())
config.plugins.IPAudio.lastAudioChannel = ConfigText(default="")  # Store last selected audio URL
config.plugins.IPAudio.equalizer = ConfigSelection(default="off", choices=[
    ("off", _("Off")),
    ("bass_boost", _("Bass Boost")),
    ("treble_boost", _("Treble Boost")),
    ("vocal", _("Vocal Enhance")),
    ("rock", _("Rock")),
    ("pop", _("Pop")),
    ("classical", _("Classical")),
    ("jazz", _("Jazz")),
])
# Picon path configuration
config.plugins.IPAudio.piconPath = ConfigSelection(default="/usr/lib/enigma2/python/Plugins/Extensions/IPAudio/picons/", choices=[
    ("/usr/share/enigma2/ipaudio/picon/", _("/usr/share/enigma2/ipaudio/picon/")),
    ("/media/hdd/ipaudio/ipaudio/picon/", _("/media/hdd/ipaudio/picon/")),
    ("/media/usb/ipaudio/ipudio/picon/", _("/media/usb/ipaudio/picon/")),
    ("/media/mmc/ipaudio/picon/", _("/media/mmc/ipaudio/picon/")),
    ("/media/sdcard/ipaudio/picon/", _("/media/sdcard/ipaaudio/picon/")),
    ("/media/sda1/ipaudio/picon/", _("/media/sda1/ipaudio/picon/")),
    ("/etc/enigma2/ipaudio/picon/", _("/etc/enigma2/ipaudio/picon/")),
    ("/usr/lib/enigma2/python/Plugins/Extensions/IPAudio/picons/", _("Plugin Folder"))
])
# Settings directory configuration
config.plugins.IPAudio.settingsPath = ConfigSelection(default="/etc/enigma2/ipaudio/", choices=[
    ("/etc/enigma2/ipaudio/", _("/etc/enigma2/ipaudio/")),
    ("/media/hdd/ipaudio/", _("/media/hdd/ipaudio/")),
    ("/media/usb/ipaudio/", _("/media/usb/ipaudio/")),
    ("/media/mmc/ipaudio/", _("/media/mmc/ipaudio/")),
    ("/media/sdcard/ipaudio/", _("/media/sdcard/ipaudio/")),
    ("/media/sda1/ipaudio/", _("/media/sda1/ipaudio/")),
    ("/usr/lib/enigma2/python/Plugins/Extensions/IPAudio/settings/", _("Plugin Folder"))
])
def validateConfigValues():
    """Ensure all config values are valid on startup"""
    if config.plugins.IPAudio.tsDelay.value is None:
        config.plugins.IPAudio.tsDelay.value = 5
        config.plugins.IPAudio.tsDelay.save()
    
    if config.plugins.IPAudio.audioDelay.value is None:
        config.plugins.IPAudio.audioDelay.value = 0
        config.plugins.IPAudio.audioDelay.save()
    
    if config.plugins.IPAudio.volLevel.value is None:
        config.plugins.IPAudio.volLevel.value = 50
        config.plugins.IPAudio.volLevel.save()

# Call on plugin load
validateConfigValues()
REDC = '\033[31m'
ENDC = '\033[m'


def cprint(text):
    print(REDC + text + ENDC)


def trace_error():
    import sys
    import traceback
    try:
        traceback.print_exc(file=sys.stdout)
        traceback.print_exc(file=open('/tmp/IPAudio.log', 'a'))
    except:
        pass

def getPlaylistDir():
    """Get the configured playlist directory"""
    path = config.plugins.IPAudio.settingsPath.value
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            pass
    return path

def getPlaylistFiles():
    """Get all playlist JSON files from the ipaudio directory"""
    import glob
    
    # Use configurable directory
    playlist_dir = getPlaylistDir()
    
    # Create directory if it doesn't exist
    if not os.path.exists(playlist_dir):
        try:
            os.makedirs(playlist_dir)
        except:
            pass
    
    playlist_files = glob.glob(playlist_dir + 'ipaudio_*.json')
    playlists = []
    for filepath in sorted(playlist_files):
        # Extract category name from filename: ipaudio_sport.json -> Sport
        filename = os.path.basename(filepath)
        category = filename.replace('ipaudio_', '').replace('.json', '')
        category = category.capitalize()  # Sport, Quran, etc.
        playlists.append({'name': category, 'file': filepath})
    
    return playlists

def getPlaylist(category_file=None):
    """Load playlist from specific file or default"""
    if category_file is None:
        # Use configurable path for default
        category_file = os.path.join(config.plugins.IPAudio.settingsPath.value, 'ipaudio.json')
    
    if fileExists(category_file):
        with open(category_file, 'r') as f:
            try:
                return json.loads(f.read())
            except ValueError:
                trace_error()
    return None


def getversioninfo():
    """Read version from version file"""
    import os
    currversion = "1.0"
    versionfile = "/usr/lib/enigma2/python/Plugins/Extensions/IPAudio/version"
    
    if os.path.exists(versionfile):
        try:
            with open(versionfile, 'r') as fp:
                for line in fp.readlines():
                    if 'version=' in line:
                        currversion = line.split('=')[1].strip()
                        break
        except:
            pass
    
    return currversion

Ver = getversioninfo()

def getPiconPath(serviceName):
    """Find picon for service name"""
    # Use configurable picon path plus plugin default
    picon_paths = [
        config.plugins.IPAudio.piconPath.value,  # User configured path
        '/usr/lib/enigma2/python/Plugins/Extensions/IPAudio/picons/'  # Plugin default
    ]
    
    # Clean service name for picon filename
    clean_name = serviceName.lower().replace(' ', '_').replace('+', 'plus')
    clean_name = ''.join(c for c in clean_name if c.isalnum() or c == '_')
    
    for path in picon_paths:
        if os.path.exists(path):
            # Try exact match
            picon_file = os.path.join(path, clean_name + '.png')
            if os.path.exists(picon_file):
                return picon_file
            
            # Try finding partial match
            try:
                for filename in os.listdir(path):
                    if clean_name in filename.lower() and filename.endswith('.png'):
                        return os.path.join(path, filename)
            except:
                pass
    
    # Return default picon if not found
    default_picon = '/usr/lib/enigma2/python/Plugins/Extensions/IPAudio/default_picon.png'
    if os.path.exists(default_picon):
        return default_picon
    
    return None

def getVideoDelayFile():
    """Get the configured video delay file path"""
    return os.path.join(config.plugins.IPAudio.settingsPath.value, 'video_delay_channels.json')

def loadVideoDelayData():
    """Load video delay data from JSON file"""
    videodelayfile = getVideoDelayFile()
    settings_dir = config.plugins.IPAudio.settingsPath.value
    
    if not os.path.exists(settings_dir):
        try:
            os.makedirs(settings_dir)
        except:
            pass
    
    if fileExists(videodelayfile):
        try:
            with open(videodelayfile, 'r') as f:
                return json.load(f)
        except:
            trace_error()
    return {}

def saveVideoDelayData(data):
    """Save video delay data to JSON file"""
    videodelayfile = getVideoDelayFile()
    settings_dir = config.plugins.IPAudio.settingsPath.value
    
    try:
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)
        with open(videodelayfile, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except:
        trace_error()
    return False

def getVideoDelayForChannel(service_ref, fallback=None):
    """Get saved video delay for a specific channel with fallback"""
    if not service_ref:
        return fallback if fallback is not None else 5  # Default to 5 seconds
    
    ref_str = service_ref.toString()
    data = loadVideoDelayData()
    
    if ref_str in data:
        delay_value = data[ref_str]
        # Validate the value
        if delay_value is not None and isinstance(delay_value, (int, float)):
            cprint("[IPAudio] Found saved video delay for channel: {} = {}".format(ref_str, delay_value))
            return int(delay_value)
    
    # No saved delay for this channel, use fallback
    if fallback is not None:
        cprint("[IPAudio] No saved delay for channel, using fallback: {}".format(fallback))
        return fallback
    
    # Final fallback
    return 5  # Default 5 seconds

def saveVideoDelayForChannel(service_ref, delay_value):
    """Save video delay for a specific channel"""
    if not service_ref:
        return False
    
    ref_str = service_ref.toString()
    data = loadVideoDelayData()
    data[ref_str] = delay_value
    
    if saveVideoDelayData(data):
        cprint("[IPAudio] Saved video delay for channel: {} = {}".format(ref_str, delay_value))
        return True
    
    return False

def getAudioBitrate(url):
    """Get audio bitrate from stream URL using ffprobe"""
    try:
        # Use ffprobe to get audio bitrate
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'a:0',  # First audio stream
            '-show_entries', 'stream=bit_rate',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            url
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        
        if result.returncode == 0:
            bitrate_bps = result.stdout.decode('utf-8').strip()
            if bitrate_bps and bitrate_bps != 'N/A':
                # Convert bps to kbps
                bitrate_kbps = int(bitrate_bps) // 1000
                return bitrate_kbps
        
        # Fallback: Try to get format bitrate if stream bitrate not available
        cmd_format = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=bit_rate',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            url
        ]
        
        result = subprocess.run(
            cmd_format,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        
        if result.returncode == 0:
            bitrate_bps = result.stdout.decode('utf-8').strip()
            if bitrate_bps and bitrate_bps != 'N/A':
                bitrate_kbps = int(bitrate_bps) // 1000
                return bitrate_kbps
        
    except Exception as e:
        cprint("[IPAudio] Error getting bitrate: {}".format(str(e)))
    
    return None  # Unknown bitrate


def isMutable():
    if fileExists('/proc/stb/info/boxtype') and open('/proc/stb/info/boxtype').read().strip() in ('sf8008', 'sf8008m', 'viper4kv20', 'beyonwizv2', 'ustym4kpro', 'gbtrio4k', 'spider-x',):
        return True
    else:
        return False


def getDesktopSize():
    s = getDesktop(0).size()
    return (s.width(), s.height())


def isHD():
    """Check if HD or FHD resolution"""
    desktopSize = getDesktopSize()
    return desktopSize[0] == 1280

class IPAudioSetup(Screen, ConfigListScreen):
    def __init__(self, session):
        Screen.__init__(self, session)
        self.currentSkin = config.plugins.IPAudio.skin.value
        
        # REPLACE THIS SECTION:
        if isHD():
            if config.plugins.IPAudio.skin.value == 'orange':
                self.skin = SKIN_IPAudioSetup_ORANGE_HD
            elif config.plugins.IPAudio.skin.value == 'teal':
                self.skin = SKIN_IPAudioSetup_TEAL_HD
            elif config.plugins.IPAudio.skin.value == 'lime':
                self.skin = SKIN_IPAudioSetup_LIME_HD
            else:
                self.skin = SKIN_IPAudioSetup_ORANGE_HD
        else:
            if config.plugins.IPAudio.skin.value == 'orange':
                self.skin = SKIN_IPAudioSetup_ORANGE_FHD
            elif config.plugins.IPAudio.skin.value == 'teal':
                self.skin = SKIN_IPAudioSetup_TEAL_FHD
            elif config.plugins.IPAudio.skin.value == 'lime':
                self.skin = SKIN_IPAudioSetup_LIME_FHD
            else:
                self.skin = SKIN_IPAudioSetup_ORANGE_FHD
        
        self.skinName = "IPAudioSetup"
        self.onChangedEntry = []
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=session, on_change=self.changedEntry)
        self["actions"] = ActionMap(["SetupActions"],
            {
                "cancel": self.keyCancel,
                "save": self.apply,
                "ok": self.apply,
            }, -2)
        # ADD THESE LINES FOR BUTTONS:
        self["key_green"] = StaticText(_("Save"))
        self["key_red"] = StaticText(_("Cancel"))
        self.configChanged = False
        self.createSetup()

    def createSetup(self):
        self.list = [getConfigListEntry(_("Player"), config.plugins.IPAudio.player)]
        if config.plugins.IPAudio.player.value == "gst1.0-ipaudio":
            self.list.append(getConfigListEntry(_("Sync Audio using"), config.plugins.IPAudio.sync))
            self.list.append(getConfigListEntry(_("Audio Equalizer"), config.plugins.IPAudio.equalizer))  # NEW
        self.list.append(getConfigListEntry(_("External links volume level"), config.plugins.IPAudio.volLevel))
        self.list.append(getConfigListEntry(_("Keep original channel audio"), config.plugins.IPAudio.keepaudio))
        self.list.append(getConfigListEntry(_("Video Delay"), config.plugins.IPAudio.tsDelay))
        self.list.append(getConfigListEntry(_("Audio Delay"), config.plugins.IPAudio.audioDelay))
        self.list.append(getConfigListEntry(_("Picons Folder"), config.plugins.IPAudio.piconPath))
        self.list.append(getConfigListEntry(_("Settings Folder"), config.plugins.IPAudio.settingsPath))
        self.list.append(getConfigListEntry(_("Remove/Reset Playlist"), config.plugins.IPAudio.playlist))
        self.list.append(getConfigListEntry(_("Enable/Disable online update"), config.plugins.IPAudio.update))
        self.list.append(getConfigListEntry(_("Show IPAudio in main menu"), config.plugins.IPAudio.mainmenu))
        self.list.append(getConfigListEntry(_("Select Your IPAudio Skin"), config.plugins.IPAudio.skin))
        self["config"].list = self.list
        self["config"].setList(self.list)

    def apply(self):
        current = self["config"].getCurrent()
        if current[1] == config.plugins.IPAudio.playlist:
            self.session.open(IPAudioPlaylist)
        else:
            # Check if paths changed
            old_picon_path = config.plugins.IPAudio.piconPath.value
            old_settings_path = config.plugins.IPAudio.settingsPath.value
            
            for x in self["config"].list:
                if len(x) > 1:
                    x[1].save()
            configfile.save()
            
            # Create directories if they don't exist
            new_settings_path = config.plugins.IPAudio.settingsPath.value
            new_picon_path = config.plugins.IPAudio.piconPath.value
            
            if not os.path.exists(new_settings_path):
                try:
                    os.makedirs(new_settings_path)
                    self.session.open(MessageBox, _("Settings folder created: {}".format(new_settings_path)), MessageBox.TYPE_INFO, timeout=3)
                except:
                    self.session.open(MessageBox, _("Failed to create settings folder: {}".format(new_settings_path)), MessageBox.TYPE_ERROR, timeout=5)
            
            if not os.path.exists(new_picon_path):
                self.session.open(MessageBox, _("Picon folder does not exist: {}\nPlease create it manually.".format(new_picon_path)), MessageBox.TYPE_WARNING, timeout=5)
            
            # Check if skin changed
            if self.currentSkin != config.plugins.IPAudio.skin.value:
                self.session.open(MessageBox, _("Skin changed! Please restart IPAudio plugin for changes to take effect."), MessageBox.TYPE_INFO, timeout=5)
            
            # Check if paths changed
            if old_settings_path != new_settings_path:
                self.session.open(MessageBox, _("Settings folder changed! Existing playlists and delays in old location will not be moved automatically."), MessageBox.TYPE_INFO, timeout=8)
            
            # Close only settings screen, not the main plugin
            self.close(False)

    def keyCancel(self):
        # Revert changes on cancel
        for x in self["config"].list:
            if len(x) > 1:
                x[1].cancel()
        self.close(False)

    def changedEntry(self):
        # This is called when any setting changes
        for x in self.onChangedEntry:
            x()
        # Rebuild the list when player changes to show/hide sync option
        current = self["config"].getCurrent()
        if current[1] == config.plugins.IPAudio.player:
            self.createSetup()

class IPAudioScreen(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        
        # REPLACE THIS SECTION:
        if isHD():
            if config.plugins.IPAudio.skin.value == 'orange':
                self.skin = SKIN_IPAudioScreen_ORANGE_HD
            elif config.plugins.IPAudio.skin.value == 'teal':
                self.skin = SKIN_IPAudioScreen_TEAL_HD
            elif config.plugins.IPAudio.skin.value == 'lime':
                self.skin = SKIN_IPAudioScreen_LIME_HD
            else:
                self.skin = SKIN_IPAudioScreen_ORANGE_HD
        else:
            if config.plugins.IPAudio.skin.value == 'orange':
                self.skin = SKIN_IPAudioScreen_ORANGE_FHD
            elif config.plugins.IPAudio.skin.value == 'teal':
                self.skin = SKIN_IPAudioScreen_TEAL_FHD
            elif config.plugins.IPAudio.skin.value == 'lime':
                self.skin = SKIN_IPAudioScreen_LIME_FHD
            else:
                self.skin = SKIN_IPAudioScreen_ORANGE_FHD
        
        self.choices = list(self.getHosts())
        self.plIndex = 0
        self['title'] = Label()  # ADD THIS
        self['title'].setText('IPAudio v{}'.format(Ver))  # ADD THIS
        self['server'] = Label()
        self['sync'] = Label()

        # NEW: Load video delay for current channel with fallback to config value
        current_service = self.session.nav.getCurrentlyPlayingServiceReference()
        # Ensure config has valid value
        if config.plugins.IPAudio.tsDelay.value is None:
            config.plugins.IPAudio.tsDelay.value = 5
            config.plugins.IPAudio.tsDelay.save()
        current_delay = config.plugins.IPAudio.tsDelay.value  # Current config value as fallback
        
        # Try to get saved delay for this channel, fallback to current config
        loaded_delay = getVideoDelayForChannel(current_service, fallback=current_delay)
        # Ensure loaded_delay is valid
        if loaded_delay is None:
            loaded_delay = 5
        
        # Update config with loaded delay (either saved or fallback)
        config.plugins.IPAudio.tsDelay.value = loaded_delay
        
        # Display real seconds (no conversion)
        self['sync'].setText('Video Delay: {}s'.format(config.plugins.IPAudio.tsDelay.value))
        # Ensure audio delay is also valid
        if config.plugins.IPAudio.audioDelay.value is None:
            config.plugins.IPAudio.audioDelay.value = 0
            config.plugins.IPAudio.audioDelay.save()        
        self['audio_delay'] = Label()
        # Display audio delay in seconds
        self['audio_delay'].setText('Audio Delay: {}s'.format(config.plugins.IPAudio.audioDelay.value))
        self['network_status'] = Label()  # For network status
        self['network_status'].setText('')
        # ADD COUNTDOWN WIDGET
        self['countdown'] = Label()
        self['countdown'].setText('')
        
        self["list"] = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        
        if isHD():
            self["list"].l.setItemHeight(40)
            self["list"].l.setFont(0, gFont('Regular', 20))
        else:
            self["list"].l.setItemHeight(50)
            self["list"].l.setFont(0, gFont('Regular', 28))
        
        self["key_red"] = Button(_("Exit"))
        self["key_green"] = Button(_("Reset Audio"))
        self["key_yellow"] = Button(_("Help"))
        self["key_blue"] = Button(_("Info"))
        self["key_menu"] = Button(_("Menu"))
        self["IPAudioAction"] = ActionMap(["IPAudioActions", "ColorActions"],
            {
                "ok": self.ok,
                "ok_long": boundFunction(self.ok, long=True),
                "cancel": self.exit,
                "menu": self.openConfig,
                "red": self.exit,        # ADD THIS - Red button exits
                "green": self.resetAudio,
                "yellow": self.showHelp,  # ADD THIS
                "blue": self.showInfo,    # ADD THIS
                "right": self.right,
                "left": self.left,
                "pause": self.pause,
                "pauseAudio": self.pauseAudioProcess,
                "delayUP": self.delayUP,
                "delayDown": self.delayDown,
                "audioDelayDown": self.audioDelayDown,
                "audioDelayReset": self.audioDelayReset,
                "audioDelayUp": self.audioDelayUp,
                "clearVideoDelay": self.clearVideoDelay,
            }, -1)
        
        self.alsa = None
        self.audioPaused = False
        self.audio_process = None
        self.radioList = []
        self.guide = dict()

        # ADD COUNTDOWN TRACKING
        self.currentDelaySeconds = 0  # Current active delay
        self.targetDelaySeconds = 0   # Target delay we want to reach
        self.countdownValue = 0
        # NEW: Add bitrate tracking
        self.currentBitrate = None
        self.bitrateCheckTimer = eTimer()
        try:
            self.bitrateCheckTimer.callback.append(self.checkAudioBitrate)
        except:
            self.bitrateCheckTimer_conn = self.bitrateCheckTimer.timeout.connect(self.checkAudioBitrate)        
        
        if HAVE_EALSA:
            self.alsa = eAlsaOutput.getInstance()
        
        # Initialize all timers
        self.timeShiftTimer = eTimer()
        self.guideTimer = eTimer()
        self.statusTimer = eTimer()
        self.countdownTimer = eTimer()  # ADD THIS
        
        try:
            self.timeShiftTimer.callback.append(self.unpauseService)
            self.guideTimer.callback.append(self.getGuide)
            self.statusTimer.callback.append(self.checkNetworkStatus)
            self.countdownTimer.callback.append(self.updateCountdown)  # ADD THIS
        except:
            self.timeShiftTimer_conn = self.timeShiftTimer.timeout.connect(self.unpauseService)
            self.guideTimer_conn = self.guideTimer.timeout.connect(self.getGuide)
            self.statusTimer_conn = self.statusTimer.timeout.connect(self.checkNetworkStatus)
            self.countdownTimer_conn = self.countdownTimer.timeout.connect(self.updateCountdown)  # ADD THIS
        
        self.lastservice = self.session.nav.getCurrentlyPlayingServiceReference()
        
        if config.plugins.IPAudio.update.value:
            self.checkupdates()
        
        self.onLayoutFinish.append(self.getGuide)
        self.onShown.append(self.onWindowShow)

    def updateCountdown(self):
        """Update countdown display every second"""
        if self.countdownValue > 0:
            self['countdown'].setText('TimeShift: {}s'.format(self.countdownValue))
            self.countdownValue -= 1
            self.countdownTimer.start(1000, True)  # Single shot, 1 second
        else:
            self['countdown'].setText('')
            self.countdownTimer.stop()

    def startCountdown(self, seconds):
        """Start countdown timer"""
        if seconds > 0:
            self.countdownValue = int(seconds)
            self.countdownTimer.start(100, True)  # Start after 100ms
            self.updateCountdown()

    def showInfo(self):
        """Open info/about screen"""
        self.session.open(IPAudioInfo)

    def showHelp(self):
        """Open help screen"""
        self.session.open(IPAudioHelp)

    def checkNetworkStatus(self):
        """Check if audio stream is still playing with bitrate info"""
        if self.audio_process:
            # Check if process is still running
            if self.audio_process.poll() is None:
                # Process is running
                if self.currentBitrate is not None:
                    self['network_status'].setText('● Playing {}kb/s'.format(self.currentBitrate))
                else:
                    self['network_status'].setText('● Playing')
            else:
                self['network_status'].setText('✗ Stopped')
                self.audio_process = None
                self.currentBitrate = None
        else:
            self['network_status'].setText('')
            self.currentBitrate = None

    def checkAudioBitrate(self):
        """Check audio bitrate of current stream"""
        if hasattr(self, 'url') and self.url and config.plugins.IPAudio.running.value:
            cprint("[IPAudio] Checking bitrate for: {}".format(self.url))
            
            # Get bitrate in background thread to avoid blocking
            bitrate = getAudioBitrate(self.url)
            
            if bitrate:
                self.currentBitrate = bitrate
                cprint("[IPAudio] Detected bitrate: {} kb/s".format(bitrate))
                # Update display immediately
                if self.audio_process and self.audio_process.poll() is None:
                    self['network_status'].setText('● Playing {}kb/s'.format(self.currentBitrate))
            else:
                cprint("[IPAudio] Could not detect bitrate")
                self.currentBitrate = None
        
        # Stop timer after first check
        self.bitrateCheckTimer.stop()

    def getTimeshift(self):
        service = self.session.nav.getCurrentService()
        return service and service.timeshift()

    def pauseAudioProcess(self):
        if config.plugins.IPAudio.running.value and IPAudioHandler.container.running():
            pid = IPAudioHandler.container.getPID()
            if not self.audioPaused:
                cmd = "kill -STOP {}".format(pid)
                self.audioPaused = True
            else:
                cmd = "kill -CONT {}".format(pid)
                self.audioPaused = False
            eConsoleAppContainer().execute(cmd)

    def pause(self):
        """Activate TimeShift with smart delay calculation"""
        if config.plugins.IPAudio.running.value:
            ts = self.getTimeshift()
            
            if ts is None:
                return
            
            # Use real seconds directly (no conversion)
            self.targetDelaySeconds = config.plugins.IPAudio.tsDelay.value
            
            if not ts.isTimeshiftEnabled():
                # First time activation - full delay
                cprint("[IPAudio] Starting TimeShift with {}s delay".format(self.targetDelaySeconds))
                
                ts.startTimeshift()
                ts.activateTimeshift()
                
                delay_ms = int(self.targetDelaySeconds * 1000)
                self.timeShiftTimer.start(delay_ms, False)
                
                # Start countdown
                self.startCountdown(self.targetDelaySeconds)
                self.currentDelaySeconds = self.targetDelaySeconds
                
            elif ts.isTimeshiftEnabled() and not self.timeShiftTimer.isActive():
                # TimeShift already active - calculate difference
                delay_difference = self.targetDelaySeconds - self.currentDelaySeconds
                
                if abs(delay_difference) < 0.5:  # Already at target (tolerance 0.5s)
                    cprint("[IPAudio] Already at target delay {}s".format(self.targetDelaySeconds))
                    return
                
                if delay_difference > 0:
                    # Need MORE delay - pause and wait for difference
                    cprint("[IPAudio] Increasing delay by {}s (from {}s to {}s)".format(
                        delay_difference, self.currentDelaySeconds, self.targetDelaySeconds))
                    
                    service = self.session.nav.getCurrentService()
                    pauseable = service.pause()
                    if pauseable:
                        pauseable.pause()
                    
                    # Only wait for the additional time needed
                    additional_delay_ms = int(delay_difference * 1000)
                    self.timeShiftTimer.start(additional_delay_ms, False)
                    
                    # Countdown for additional delay only
                    self.startCountdown(delay_difference)
                    self.currentDelaySeconds = self.targetDelaySeconds
                    
                else:
                    # Need LESS delay - restart TimeShift with new delay
                    cprint("[IPAudio] Decreasing delay to {}s (was {}s)".format(
                        self.targetDelaySeconds, self.currentDelaySeconds))
                    
                    ts.stopTimeshift()
                    ts.startTimeshift()
                    ts.activateTimeshift()
                    
                    delay_ms = int(self.targetDelaySeconds * 1000)
                    self.timeShiftTimer.start(delay_ms, False)
                    
                    # Countdown for new delay
                    self.startCountdown(self.targetDelaySeconds)
                    self.currentDelaySeconds = self.targetDelaySeconds

    def unpauseService(self):
        self.timeShiftTimer.stop()
        service = self.session.nav.getCurrentService()
        pauseable = service.pause()
        if pauseable:
            pauseable.unpause()

    def delayUP(self):
        """Increase TimeShift delay by 1 second"""
        # Safety check
        if config.plugins.IPAudio.tsDelay.value is None:
            config.plugins.IPAudio.tsDelay.value = 5
        
        if config.plugins.IPAudio.tsDelay.value < 300:  # Max 300 seconds
            config.plugins.IPAudio.tsDelay.value += 1  # Add 1 second
            config.plugins.IPAudio.tsDelay.save()
            
            # Display in seconds
            self['sync'].setText('Video Delay: {}s'.format(config.plugins.IPAudio.tsDelay.value))
            
            # Save delay for current channel
            current_service = self.session.nav.getCurrentlyPlayingServiceReference()
            saveVideoDelayForChannel(current_service, config.plugins.IPAudio.tsDelay.value)

    def delayDown(self):
        """Decrease TimeShift delay by 1 second"""
        # Safety check
        if config.plugins.IPAudio.tsDelay.value is None:
            config.plugins.IPAudio.tsDelay.value = 5
        
        if config.plugins.IPAudio.tsDelay.value > 0:  # Min 0 seconds
            config.plugins.IPAudio.tsDelay.value -= 1  # Subtract 1 second
            config.plugins.IPAudio.tsDelay.save()
            
            # Display in seconds
            self['sync'].setText('Video Delay: {}s'.format(config.plugins.IPAudio.tsDelay.value))
            
            # Save delay for current channel
            current_service = self.session.nav.getCurrentlyPlayingServiceReference()
            saveVideoDelayForChannel(current_service, config.plugins.IPAudio.tsDelay.value)

    def getHosts(self):
        """Get all available playlists including custom categories"""
        hosts = resolveFilename(SCOPE_PLUGINS, "Extensions/IPAudio/hosts.json")
        self.hosts = None
        
        if fileExists(hosts):
            hosts = open(hosts, 'r').read()
            self.hosts = json.loads(hosts, object_pairs_hook=OrderedDict)
            for host in self.hosts:
                yield host
        
        # Add custom playlist categories
        custom_playlists = getPlaylistFiles()
        for playlist in custom_playlists:
            yield playlist['name']

    def onWindowShow(self):
        self.onShown.remove(self.onWindowShow)
        self.guideTimer.start(30000)
        
        # Check and update video delay for current channel with fallback
        current_service = self.session.nav.getCurrentlyPlayingServiceReference()
        current_delay = config.plugins.IPAudio.tsDelay.value  # Use current as fallback
        
        # Get saved delay or use current config as fallback
        loaded_delay = getVideoDelayForChannel(current_service, fallback=current_delay)
        
        # Update display - real seconds
        config.plugins.IPAudio.tsDelay.value = loaded_delay
        self['sync'].setText('Video Delay: {}s'.format(config.plugins.IPAudio.tsDelay.value))
        
        # NEW: Try to restore last selected audio channel
        restored = False
        
        if config.plugins.IPAudio.lastAudioChannel.value:
            last_url = config.plugins.IPAudio.lastAudioChannel.value
            cprint("[IPAudio] Attempting to restore last audio channel: {}".format(last_url))
            
            # First, try to restore from lastidx (playlist + channel index)
            if config.plugins.IPAudio.lastidx.value:
                try:
                    lastplaylist, lastchannel = map(int, config.plugins.IPAudio.lastidx.value.split(','))
                    self.plIndex = lastplaylist
                    self.changePlaylist()
                    
                    # Verify the channel at this index matches the saved URL
                    if len(self.radioList) > lastchannel:
                        if self.radioList[lastchannel][1] == last_url:
                            self['list'].moveToIndex(lastchannel)
                            cprint("[IPAudio] Restored to playlist {} channel {}".format(lastplaylist, lastchannel))
                            restored = True
                        else:
                            # Index doesn't match, search for URL
                            cprint("[IPAudio] Index mismatch, searching for URL in current playlist")
                            for idx, channel in enumerate(self.radioList):
                                if channel[1] == last_url:
                                    self['list'].moveToIndex(idx)
                                    cprint("[IPAudio] Found channel at index {}".format(idx))
                                    restored = True
                                    break
                except Exception as e:
                    cprint("[IPAudio] Error restoring from lastidx: {}".format(str(e)))
            
            # If not restored yet, search all playlists for the URL
            if not restored:
                cprint("[IPAudio] Searching all playlists for last audio channel")
                found = False
                
                for playlist_idx, playlist_name in enumerate(self.choices):
                    self.plIndex = playlist_idx
                    self.changePlaylist()
                    
                    # Search in current playlist
                    for channel_idx, channel in enumerate(self.radioList):
                        if channel[1] == last_url:
                            self['list'].moveToIndex(channel_idx)
                            cprint("[IPAudio] Found in playlist '{}' at index {}".format(playlist_name, channel_idx))
                            
                            # Update lastidx to new position
                            config.plugins.IPAudio.lastidx.value = '{},{}'.format(playlist_idx, channel_idx)
                            config.plugins.IPAudio.lastidx.save()
                            
                            found = True
                            restored = True
                            break
                    
                    if found:
                        break
                
                if not restored:
                    cprint("[IPAudio] Could not find last audio channel, using first available")
        
        # Fallback: If not restored, use first playlist and first channel
        if not restored:
            if config.plugins.IPAudio.lastidx.value:
                try:
                    lastplaylist, lastchannel = map(int, config.plugins.IPAudio.lastidx.value.split(','))
                    self.plIndex = lastplaylist
                    self.changePlaylist()
                    self['list'].moveToIndex(lastchannel)
                    cprint("[IPAudio] Using lastidx fallback: playlist {} channel {}".format(lastplaylist, lastchannel))
                except:
                    self.setPlaylist()
            else:
                self.setPlaylist()

    def clearVideoDelay(self):
        """Clear saved video delay for current channel"""
        current_service = self.session.nav.getCurrentlyPlayingServiceReference()
        if current_service:
            ref_str = current_service.toString()
            data = loadVideoDelayData()
            
            if ref_str in data:
                del data[ref_str]
                saveVideoDelayData(data)
                cprint("[IPAudio] Cleared saved delay for channel: {}".format(ref_str))
                self.session.open(MessageBox, _("Video delay cleared for this channel"), MessageBox.TYPE_INFO, timeout=3)
            else:
                self.session.open(MessageBox, _("No saved delay for this channel"), MessageBox.TYPE_INFO, timeout=3)

    def checkupdates(self):
        """Check for plugin updates from GitHub"""
        url = "https://raw.githubusercontent.com/popking159/ipaudio/main/installer-ipaudio.sh"
        self.callUrl(url, self.checkVer)

    def checkVer(self, data):
        """Parse version from installer script"""
        try:
            if PY3:
                data = data.decode('utf-8')
            else:
                data = data.encode('utf-8')
            
            if data:
                lines = data.split('\n')
                self.newversion = None
                self.newdescription = ""
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('version='):
                        # Extract version: version="8.1"
                        self.newversion = line.split('=')[1].strip('"').strip("'")
                    elif line.startswith('description='):
                        # Extract description: description="New features"
                        self.newdescription = line.split('=')[1].strip('"').strip("'")
                
                if self.newversion:
                    cprint("[IPAudio] Current version: {}, New version: {}".format(Ver, self.newversion))
                    
                    # Compare versions
                    try:
                        current = float(Ver)
                        new = float(self.newversion)
                        
                        if new > current:
                            msg = "New version {} is available.\n\n{}\n\nDo you want to install it now?".format(
                                self.newversion, 
                                self.newdescription
                            )
                            self.session.openWithCallback(
                                self.installupdate, 
                                MessageBox, 
                                msg, 
                                MessageBox.TYPE_YESNO
                            )
                    except ValueError:
                        cprint("[IPAudio] Could not compare versions")
        except Exception as e:
            cprint("[IPAudio] Error checking version: {}".format(str(e)))
            trace_error()

    def installupdate(self, answer=False):
        """Install update from GitHub"""
        if answer:
            url = "https://raw.githubusercontent.com/popking159/ipaudio/main/installer-ipaudio.sh"
            cmdlist = []
            cmdlist.append('wget -q --no-check-certificate {} -O - | bash'.format(url))
            self.session.open(
                Console2, 
                title="Update IPAudio", 
                cmdlist=cmdlist, 
                closeOnSuccess=False
            )

    def callUrl(self, url, callback):
        try:
            from twisted.web.client import getPage
            getPage(str.encode(url), headers={b'Content-Type': b'application/x-www-form-urlencoded'}).addCallback(callback).addErrback(self.addErrback)
        except:
            pass

    def getAnisUrls(self):
        """Fetch Anis playlist from GitHub"""
        url = "https://raw.githubusercontent.com/popking159/ipaudio/refs/heads/main/ipaudio_anis.json"
        self.callUrl(url, self.parseAnisData)

    def parseAnisData(self, data):
        """Parse Anis JSON data from GitHub"""
        try:
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            
            playlist_data = json.loads(data)
            list = []
            
            if 'playlist' in playlist_data:
                for channel in playlist_data['playlist']:
                    try:
                        list.append([str(channel['channel']), str(channel['url'])])
                    except KeyError:
                        pass
            
            if len(list) > 0:
                self["list"].l.setList(self.iniMenu(list))
                self["list"].show()
                self.radioList = list
            else:
                self["list"].hide()
                self.radioList = []
                self['server'].setText('Anis Sport - Playlist is empty')
        except Exception as e:
            cprint("[IPAudio] Error parsing Anis data: {}".format(str(e)))
            trace_error()
            self["list"].hide()
            self.radioList = []
            self['server'].setText('Error loading Anis Sport')

    def addErrback(self, error=None):
        pass

    def right(self):
        self.plIndex += 1
        self.changePlaylist()

    def left(self):
        self.plIndex -= 1
        self.changePlaylist()

    def changePlaylist(self):
        if self.plIndex > len(self.choices) - 1:
            self.plIndex = 0
        if self.plIndex < 0:
            self.plIndex = len(self.choices) - 1
        
        # Reset radioList when changing playlist
        self.radioList = []
        self.setPlaylist()

    def setPlaylist(self):
        current = self.choices[self.plIndex]
        
        if current in self.hosts:
            if current in ["Anis Sport"]:
                self.getAnisUrls()
                self['server'].setText(str(current))
            else:
                list = []
                for cmd in self.hosts[current]['cmds']:
                    list.append([cmd.split('|')[0], cmd.split('|')[1]])
                list = self.checkINGuide(list)
                
                if len(list) > 0:  # Add check
                    self["list"].l.setList(self.iniMenu(list))
                    self["list"].show()
                    self.radioList = list
                    self['server'].setText(str(current))
                else:
                    self["list"].hide()
                    self.radioList = []  # Initialize empty
                    self['server'].setText('Playlist is empty')
        else:
            # Custom playlist category
            category_lower = current.lower()
            playlist_dir = getPlaylistDir()  # Use configurable path
            playlist_file = playlist_dir + 'ipaudio_{}.json'.format(category_lower)
            
            if fileExists(playlist_file):
                playlist = getPlaylist(playlist_file)
                if playlist:
                    list = []
                    for channel in playlist['playlist']:
                        try:
                            list.append([str(channel['channel']), str(channel['url'])])
                        except KeyError:
                            pass
                    
                    if len(list) > 0:
                        self["list"].l.setList(self.iniMenu(list))
                        self["list"].show()
                        self.radioList = list
                        self['server'].setText(current)
                    else:
                        self["list"].hide()
                        self.radioList = []  # Initialize empty
                        self['server'].setText('{} - Playlist is empty'.format(current))
                else:
                    self["list"].hide()
                    self.radioList = []  # Initialize empty
                    self['server'].setText('Cannot load playlist')
            else:
                self["list"].hide()
                self.radioList = []  # Initialize empty
                self['server'].setText('Playlist file not found')

    def checkINGuide(self, entries):
        for idx, entry in enumerate(entries):
            if entry[0] in self.guide:
                if self.guide[entry[0]]['check']:
                    nowIntimestamp = datetime.now().strftime('%s')
                    entryProgEnding = self.guide[entry[0]]['end']
                    if int(entryProgEnding) >= int(nowIntimestamp):
                        entries[idx] = (self.guide[entry[0]]['prog'], entry[1])
        return entries

    def getGuide(self):
        url = 'http://ipkinstall.ath.cx/ipaudio/epg.json'
        self.callUrl(url, self.parseGuide)

    def parseGuide(self, data):
        if PY3:
            data = data.decode("utf-8")
        else:
            data = data.encode("utf-8")
        self.guide = json.loads(data)
        if self.guide != {}:
            self.setPlaylist()

    def iniMenu(self, sList):
        """Initialize menu list with picons and channel names"""
        
        res = []
        gList = []
        
        for elem in sList:
            picon_path = getPiconPath(elem[0])
            
            if isHD():
                # HD resolution (1280x720) - 58px item height, 570px width
                res.append(MultiContentEntryText(
                    pos=(0, 0), 
                    size=(0, 0), 
                    font=0, 
                    flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER | RT_WRAP, 
                    text='', 
                    border_width=3
                ))
                
                # Add picon if found
                if picon_path:
                    pixmap = loadPNG(picon_path)
                    if pixmap:
                        res.append(MultiContentEntryPixmapAlphaTest(
                            pos=(10, 1), 
                            size=(100, 56), 
                            png=pixmap
                        ))
                        # Adjust text position to make room for picon
                        res.append(MultiContentEntryText(
                            pos=(120, 4), 
                            size=(440, 50), 
                            font=0, 
                            backcolor_sel=None, 
                            flags=RT_VALIGN_CENTER | RT_HALIGN_LEFT, 
                            text=str(elem[0])
                        ))
                    else:
                        res.append(MultiContentEntryText(
                            pos=(5, 4), 
                            size=(560, 50), 
                            font=0, 
                            backcolor_sel=None, 
                            flags=RT_VALIGN_CENTER | RT_HALIGN_LEFT, 
                            text=str(elem[0])
                        ))
                else:
                    res.append(MultiContentEntryText(
                        pos=(5, 4), 
                        size=(560, 50), 
                        font=0, 
                        backcolor_sel=None, 
                        flags=RT_VALIGN_CENTER | RT_HALIGN_LEFT, 
                        text=str(elem[0])
                    ))
            else:
                # FHD resolution (1920x1080) - 50px item height, 840px width
                res.append(MultiContentEntryText(
                    pos=(0, 0), 
                    size=(0, 0), 
                    font=0, 
                    flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER | RT_WRAP, 
                    text='', 
                    border_width=3
                ))
                
                # Add picon if found
                if picon_path:
                    pixmap = loadPNG(picon_path)
                    if pixmap:
                        res.append(MultiContentEntryPixmapAlphaTest(
                            pos=(10, 1), 
                            size=(110, 48), 
                            png=pixmap
                        ))
                        # Adjust text position to make room for picon
                        res.append(MultiContentEntryText(
                            pos=(130, 4), 
                            size=(700, 42), 
                            font=0, 
                            backcolor_sel=None, 
                            flags=RT_VALIGN_CENTER | RT_HALIGN_LEFT, 
                            text=str(elem[0])
                        ))
                    else:
                        res.append(MultiContentEntryText(
                            pos=(5, 4), 
                            size=(830, 42), 
                            font=0, 
                            backcolor_sel=None, 
                            flags=RT_VALIGN_CENTER | RT_HALIGN_LEFT, 
                            text=str(elem[0])
                        ))
                else:
                    res.append(MultiContentEntryText(
                        pos=(5, 4), 
                        size=(830, 42), 
                        font=0, 
                        backcolor_sel=None, 
                        flags=RT_VALIGN_CENTER | RT_HALIGN_LEFT, 
                        text=str(elem[0])
                    ))
            
            gList.append(res)
            res = []
        
        return gList

    def ok(self, long=False):
        # Check if there are any items in the list
        if not hasattr(self, 'radioList') or len(self.radioList) == 0:
            self.session.open(MessageBox, _("Playlist is empty! Please add channels first."), MessageBox.TYPE_INFO, timeout=5)
            return
        
        # Check if valid selection
        index = self['list'].getSelectionIndex()
        if index is None or index < 0 or index >= len(self.radioList):
            self.session.open(MessageBox, _("Please select a channel first."), MessageBox.TYPE_INFO, timeout=5)
            return
        
        # Determine which player to use  
        if config.plugins.IPAudio.player.value == "gst1.0-ipaudio":
            player_check = '/usr/bin/gst-launch-1.0'
        else:
            player_check = '/usr/bin/ffmpeg'
        
        if fileExists(player_check):
            currentAudioTrack = 0
            if long:
                service = self.session.nav.getCurrentService()
                if not service.streamed():
                    currentAudioTrack = service.audioTracks().getCurrentTrack()
                self.url = 'http://127.0.0.1:8001/{}'.format(self.lastservice.toString())
                config.plugins.IPAudio.lastplayed.value = "e2_service"
            else:
                try:
                    self.url = self.radioList[index][1]
                    config.plugins.IPAudio.lastplayed.value = self.url
                    config.plugins.IPAudio.lastidx.value = '{},{}'.format(self.plIndex, index)
                    config.plugins.IPAudio.lastidx.save()
                    # NEW: Save last audio channel URL
                    config.plugins.IPAudio.lastAudioChannel.value = self.url
                    config.plugins.IPAudio.lastAudioChannel.save()
                    cprint("[IPAudio] Saved last audio channel: {}".format(self.url))
                except (IndexError, KeyError) as e:
                    cprint("[IPAudio] Error accessing radioList: {}".format(str(e)))
                    self.session.open(MessageBox, _("Error selecting channel."), MessageBox.TYPE_ERROR, timeout=5)
                    return
            
            if config.plugins.IPAudio.player.value == "gst1.0-ipaudio":
                # Build equalizer string
                eq_filter = self.getEqualizerFilter()
                
                # FIXED: Calculate volume with better range
                # Level 1 = 0.2 (20%), Level 5 = 1.0 (100%), Level 10 = 2.0 (200%)
                volume = config.plugins.IPAudio.volLevel.value / 0.5
                
                # Use the WORKING GStreamer command
                sink = config.plugins.IPAudio.sync.value
                cmd = 'gst-launch-1.0 -e uridecodebin uri="{}" ! audioconvert ! audioresample ! '.format(self.url)
                
                # FIXED: Always add volume control (not just for Custom Playlist)
                cmd += 'volume volume={} ! '.format(volume)
                
                # Add equalizer if enabled
                if eq_filter:
                    cmd += '{} ! '.format(eq_filter)
                
                # Add audio delay buffer if needed
                delay_ms = config.plugins.IPAudio.audioDelay.value * 1000  # Convert seconds to ms
                if delay_ms != 0:
                    delay_ns = abs(delay_ms) * 1000000
                    if delay_ms > 0:
                        # Positive delay - buffer audio
                        cmd += 'audiobuffersplit output-buffer-duration={} ! '.format(delay_ns)
                    else:
                        # Negative delay - minimal buffer
                        cmd += 'queue max-size-buffers=1 max-size-time=1000000 ! '
                
                cmd += '{} sync=false'.format(sink)
                
                cprint("[IPAudio] GStreamer command: {}".format(cmd))
                cprint("[IPAudio] Volume level: {} = {}x".format(config.plugins.IPAudio.volLevel.value, volume))
                
            else:
                # FFmpeg command with audio delay AND volume
                delay_sec = config.plugins.IPAudio.audioDelay.value
                
                # FIXED: Calculate volume with better range
                volume = config.plugins.IPAudio.volLevel.value / 0.5
                
                if delay_sec > 0:
                    # Positive delay with volume
                    delay_ms = delay_sec * 1000
                    cmd = 'ffmpeg -i "{}" -af "adelay={}|{},volume={}" -vn -f alsa default'.format(
                        self.url, delay_ms, delay_ms, volume)
                elif delay_sec < 0:
                    # Negative delay - skip start with volume
                    trim_sec = abs(delay_sec)
                    cmd = 'ffmpeg -ss {} -i "{}" -af "volume={}" -vn -f alsa default'.format(
                        trim_sec, self.url, volume)
                else:
                    # No delay, just volume
                    cmd = 'ffmpeg -i "{}" -af "volume={}" -vn -f alsa default'.format(self.url, volume)
                
                if currentAudioTrack > 0:
                    # Add audio track selection
                    cmd = cmd.replace('-i', '-i').replace('-vn', '-map 0:a:{} -vn'.format(currentAudioTrack))
                
                cprint("[IPAudio] FFmpeg command: {}".format(cmd))
                cprint("[IPAudio] Volume level: {} = {}x".format(config.plugins.IPAudio.volLevel.value, volume))

            self.runCmd(cmd)
            # NEW: Check bitrate after starting audio
            # Wait 2 seconds for stream to stabilize, then check bitrate
            self.currentBitrate = None
            self.bitrateCheckTimer.start(2000, True)  # Single shot after 2 seconds
        else:
            self.session.open(MessageBox, _("Cannot play url, player is missing !!"), MessageBox.TYPE_ERROR, timeout=5)

    def audioReStart(self):
        cprint("[IPAudio] audioReStart called")
        
        # Kill audio process if running - aggressive approach
        if self.audio_process:
            try:
                self.audio_process.kill()
                self.audio_process.wait(timeout=1)
                self.audio_process = None
            except:
                pass
        
        # Fallback - kill all instances
        os.system("killall -9 gst-launch-1.0 ffmpeg 2>/dev/null")
        
        # Stop timeshift if active
        ts = self.getTimeshift()
        if ts and ts.isTimeshiftEnabled():
            ts.stopTimeshift()
        
        # Stop timeshift timer
        if self.timeShiftTimer.isActive():
            self.timeShiftTimer.stop()
        
        # Restore audio device
        if fileExists('/dev/dvb/adapter0/audio10') and not isMutable():
            try:
                os.rename('/dev/dvb/adapter0/audio10', '/dev/dvb/adapter0/audio0')
            except:
                pass
            
            # Restart service to restore video
            self.session.nav.stopService()
            self.restoreTimer = eTimer()
            try:
                self.restoreTimer.callback.append(self.restoreService)
            except:
                self.restoreTimer_conn = self.restoreTimer.timeout.connect(self.restoreService)
            self.restoreTimer.start(100, True)
        elif config.plugins.IPAudio.running.value and isMutable():
            if IPAudioHandler.container.running():
                IPAudioHandler.container.kill()
        
        config.plugins.IPAudio.running.value = False
        config.plugins.IPAudio.running.save()

    def resetAudio(self):
        cprint("[IPAudio] resetAudio called")
        
        # Stop status monitoring
        if self.statusTimer.isActive():
            self.statusTimer.stop()
        # NEW: Stop bitrate check
        if self.bitrateCheckTimer.isActive():
            self.bitrateCheckTimer.stop()
        
        self.currentBitrate = None  # Clear bitrate        
        # Kill audio process if running - aggressive approach
        if self.audio_process:
            try:
                cprint("[IPAudio] Terminating process PID: {}".format(self.audio_process.pid))
                # Send SIGTERM first
                self.audio_process.terminate()
                try:
                    self.audio_process.wait(timeout=1)
                    cprint("[IPAudio] Process terminated gracefully")
                except subprocess.TimeoutExpired:
                    # Force kill if still running
                    cprint("[IPAudio] Process not responding, force killing")
                    self.audio_process.kill()
                    self.audio_process.wait(timeout=1)
                    cprint("[IPAudio] Process force killed")
                self.audio_process = None
            except Exception as e:
                cprint("[IPAudio] Error killing process: {}".format(str(e)))
                # Force kill using OS command as fallback
                try:
                    os.system("killall -9 gst-launch-1.0 ffmpeg 2>/dev/null")
                except:
                    pass
                self.audio_process = None
        else:
            # No process tracked, try to kill any running instances
            cprint("[IPAudio] No process tracked, killing all gst-launch and ffmpeg")
            os.system("killall -9 gst-launch-1.0 ffmpeg 2>/dev/null")
        
        # Kill container processes
        if IPAudioHandler.container.running():
            IPAudioHandler.container.kill()
        
        # Update status
        self['network_status'].setText('')
        
        # Restore original audio and VIDEO
        if not self.alsa:
            if fileExists('/dev/dvb/adapter0/audio10') and not isMutable():
                # Restore audio device
                try:
                    os.rename('/dev/dvb/adapter0/audio10', '/dev/dvb/adapter0/audio0')
                    cprint("[IPAudio] Audio device restored")
                except:
                    pass
                
                # IMPORTANT: Restart the service to restore VIDEO
                self.session.nav.stopService()
                self.restoreTimer = eTimer()
                try:
                    self.restoreTimer.callback.append(self.restoreService)
                except:
                    self.restoreTimer_conn = self.restoreTimer.timeout.connect(self.restoreService)
                self.restoreTimer.start(100, True)
            elif isMutable():
                # For mutable boxes, just restart service to restore video
                self.session.nav.stopService()
                self.restoreTimer = eTimer()
                try:
                    self.restoreTimer.callback.append(self.restoreService)
                except:
                    self.restoreTimer_conn = self.restoreTimer.timeout.connect(self.restoreService)
                self.restoreTimer.start(100, True)
        
        config.plugins.IPAudio.running.value = False
        config.plugins.IPAudio.running.save()

    def restoreService(self):
        """Restore video service after short delay"""
        cprint("[IPAudio] Restoring service")
        self.session.nav.playService(self.lastservice)

    def runCmd(self, cmd):
        cprint("[IPAudio] runCmd called with: {}".format(cmd))
        
        # Stop any existing process first
        if self.audio_process:
            try:
                self.audio_process.terminate()
                try:
                    self.audio_process.wait(timeout=1)
                except:
                    self.audio_process.kill()
            except:
                pass
            self.audio_process = None
        
        if IPAudioHandler.container.running():
            IPAudioHandler.container.kill()
        
        if self.alsa:
            self.alsa.stop()
            self.alsa.close()
        else:
            if not config.plugins.IPAudio.keepaudio.value:
                if fileExists('/dev/dvb/adapter0/audio0') and not isMutable():
                    self.session.nav.stopService()
                    try:
                        os.rename('/dev/dvb/adapter0/audio0', '/dev/dvb/adapter0/audio10')
                    except:
                        pass
                    self.session.nav.playService(self.lastservice)
        
        # Run subprocess exactly like the working plugin
        try:
            cprint("[IPAudio] Executing subprocess...")
            self.audio_process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            cprint("[IPAudio] Process started with PID: {}".format(self.audio_process.pid))
        except Exception as e:
            cprint("[IPAudio] ERROR starting process: {}".format(str(e)))
            trace_error()
            self.audio_process = None
        
        config.plugins.IPAudio.running.value = True
        config.plugins.IPAudio.running.save()
        # Start status monitoring
        if not self.statusTimer.isActive():
            self.statusTimer.start(2000)  # Check every 2 seconds

    def audioDelayUp(self):
        """Increase audio delay by 1 second"""
        # Safety check
        if config.plugins.IPAudio.audioDelay.value is None:
            config.plugins.IPAudio.audioDelay.value = 0
        
        if config.plugins.IPAudio.audioDelay.value < 60:  # Max 60 seconds
            config.plugins.IPAudio.audioDelay.value += 1  # Add 1 second
            config.plugins.IPAudio.audioDelay.save()
            self['audio_delay'].setText('Audio Delay: {}s'.format(config.plugins.IPAudio.audioDelay.value))
            
            # If audio is playing, restart with new delay
            if config.plugins.IPAudio.running.value:
                self.restartAudioWithDelay()

    def audioDelayDown(self):
        """Decrease audio delay by 1 second"""
        # Safety check
        if config.plugins.IPAudio.audioDelay.value is None:
            config.plugins.IPAudio.audioDelay.value = 0
        
        if config.plugins.IPAudio.audioDelay.value > -10:  # Min -10 seconds
            config.plugins.IPAudio.audioDelay.value -= 1  # Subtract 1 second
            config.plugins.IPAudio.audioDelay.save()
            self['audio_delay'].setText('Audio Delay: {}s'.format(config.plugins.IPAudio.audioDelay.value))
            
            # If audio is playing, restart with new delay
            if config.plugins.IPAudio.running.value:
                self.restartAudioWithDelay()

    def audioDelayReset(self):
        """Reset audio delay to 0"""
        config.plugins.IPAudio.audioDelay.value = 0
        config.plugins.IPAudio.audioDelay.save()
        self['audio_delay'].setText('Audio Delay: 0s')
        
        # If audio is playing, restart with no delay
        if config.plugins.IPAudio.running.value:
            self.restartAudioWithDelay()

    def applyAudioDelay(self):
        """Restart audio with new delay - smooth transition"""
        if hasattr(self, 'url') and self.url:
            # Remember current URL
            current_url = self.url
            
            # Stop current audio
            if self.audio_process:
                try:
                    self.audio_process.terminate()
                    self.audio_process.wait(timeout=1)
                except:
                    try:
                        self.audio_process.kill()
                    except:
                        pass
                self.audio_process = None
            
            # Small delay before restarting
            self.delayRestartTimer = eTimer()
            try:
                self.delayRestartTimer.callback.append(lambda: self.restartAudioWithDelay(current_url))
            except:
                self.delayRestartTimer_conn = self.delayRestartTimer.timeout.connect(lambda: self.restartAudioWithDelay(current_url))
            self.delayRestartTimer.start(100, True)

    def restartAudioWithDelay(self):
        """Restart audio stream with new delay setting"""
        if hasattr(self, 'url') and self.url:
            cprint("[IPAudio] Restarting audio with new delay: {}ms".format(config.plugins.IPAudio.audioDelay.value))
            
            # Kill current audio
            if self.audio_process:
                try:
                    self.audio_process.terminate()
                    self.audio_process.wait(timeout=1)
                except:
                    pass
            
            if IPAudioHandler.container.running():
                IPAudioHandler.container.kill()
            
            # Rebuild and restart command with new delay
            delay_ms = config.plugins.IPAudio.audioDelay.value
            
            if config.plugins.IPAudio.player.value == "gst1.0-ipaudio":
                sink = config.plugins.IPAudio.sync.value
                cmd = 'gst-launch-1.0 -e uridecodebin uri="{}" ! audioconvert ! audioresample ! '.format(self.url)
                
                # Add audio delay buffer if needed
                if delay_ms != 0:
                    delay_ns = abs(delay_ms) * 1000000
                    if delay_ms > 0:
                        cmd += 'audiobuffersplit output-buffer-duration={} ! '.format(delay_ns)
                    else:
                        cmd += 'queue max-size-buffers=1 max-size-time=1000000 ! '
                
                cmd += '{} sync=false'.format(sink)
                
                # Add volume if custom playlist
                if hasattr(self, 'plIndex') and self.plIndex < len(self.choices):
                    if self.choices[self.plIndex] not in self.hosts:
                        volume = config.plugins.IPAudio.volLevel.value / 0.5
                        cmd = cmd.replace('audioresample !', 'audioresample ! volume volume={} !'.format(volume))
            else:
                # FFmpeg with delay
                if delay_ms > 0:
                    cmd = 'ffmpeg -i "{}" -af "adelay={}|{}" -vn -f alsa default'.format(self.url, delay_ms, delay_ms)
                elif delay_ms < 0:
                    trim_sec = abs(delay_ms) / 1000.0
                    cmd = 'ffmpeg -ss {} -i "{}" -vn -f alsa default'.format(trim_sec, self.url)
                else:
                    cmd = 'ffmpeg -i "{}" -vn -f alsa default'.format(self.url)
            
            self.runCmd(cmd)

    def openConfig(self):
        self.session.openWithCallback(self.configClosed, IPAudioSetup)

    def configClosed(self, ret=None):
        # Callback after settings closed - do nothing, stay in main screen
        pass

    def getEqualizerFilter(self):
        """Get GStreamer equalizer filter based on preset"""
        eq = config.plugins.IPAudio.equalizer.value
        
        if eq == "off":
            return None
        elif eq == "bass_boost":
            return "equalizer-3bands band0=-6.0 band1=-3.0 band2=6.0"
        elif eq == "treble_boost":
            return "equalizer-3bands band0=6.0 band1=-3.0 band2=-6.0"
        elif eq == "vocal":
            return "equalizer-3bands band0=-3.0 band1=6.0 band2=-3.0"
        elif eq == "rock":
            return "equalizer-3bands band0=5.0 band1=3.0 band2=-2.0"
        elif eq == "pop":
            return "equalizer-3bands band0=-2.0 band1=5.0 band2=3.0"
        elif eq == "classical":
            return "equalizer-3bands band0=4.0 band1=0.0 band2=-4.0"
        elif eq == "jazz":
            return "equalizer-3bands band0=3.0 band1=2.0 band2=4.0"
        
        return None

    def exit(self, ret=False):
        # Stop all timers
        if self.guideTimer.isActive():
            self.guideTimer.stop()
        
        if self.statusTimer.isActive():  # ADD THIS
            self.statusTimer.stop()
        
        if self.bitrateCheckTimer.isActive():  # NEW
            self.bitrateCheckTimer.stop()        
        # Just close the plugin GUI - audio continues
        if ret and not self.timeShiftTimer.isActive():
            self.close()
        else:
            self.close()


class IPAudioPlaylist(IPAudioScreen):

    def __init__(self, session):
        IPAudioScreen.__init__(self, session)
        
        # REPLACE/ADD THIS SECTION (after IPAudioScreen.__init__):
        if isHD():
            if config.plugins.IPAudio.skin.value == 'orange':
                self.skin = SKIN_IPAudioPlaylist_ORANGE_HD
            elif config.plugins.IPAudio.skin.value == 'teal':
                self.skin = SKIN_IPAudioPlaylist_TEAL_HD
            elif config.plugins.IPAudio.skin.value == 'lime':
                self.skin = SKIN_IPAudioPlaylist_LIME_HD
            else:
                self.skin = SKIN_IPAudioPlaylist_ORANGE_HD
        else:
            if config.plugins.IPAudio.skin.value == 'orange':
                self.skin = SKIN_IPAudioPlaylist_ORANGE_FHD
            elif config.plugins.IPAudio.skin.value == 'teal':
                self.skin = SKIN_IPAudioPlaylist_TEAL_FHD
            elif config.plugins.IPAudio.skin.value == 'lime':
                self.skin = SKIN_IPAudioPlaylist_LIME_FHD
            else:
                self.skin = SKIN_IPAudioPlaylist_ORANGE_FHD
        
        self["key_green"] = Button(_("Remove Link"))
        self["key_red"] = Button(_("Reset Playlist"))
        self["IPAudioAction"] = ActionMap(["IPAudioActions"],
        {
            "cancel": self.exit,
            "green": self.keyGreen,
            "red": self.keyRed,
        }, -1)
        self.onLayoutFinish = []
        self.onShown = []
        self.loadPlaylist()

    def loadPlaylist(self):
        playlist = getPlaylist()
        if playlist:
            list = []
            for channel in playlist['playlist']:
                try:
                    list.append((str(channel['channel']), str(channel['url'])))
                except KeyError:
                    pass
            if len(list) > 0:
                self["list"].l.setList(self.iniMenu(list))
                self["server"].setText('Custom Playlist')
            else:
                self["list"].hide()
                self["server"].setText('Playlist is empty')
        else:
            self["list"].hide()
            self["server"].setText('Cannot load playlist')

    def keyRed(self):
        playlist = getPlaylist()
        if playlist:
            playlist['playlist'] = []
            with open("/etc/enigma2/ipaudio.json", 'w')as f:
                json.dump(playlist, f, indent=4)
            self.loadPlaylist()

    def keyGreen(self):
        playlist = getPlaylist()
        if playlist:
            if len(playlist['playlist']) > 0:
                index = self['list'].getSelectionIndex()
                currentPlaylist = playlist["playlist"]
                del currentPlaylist[index]
                playlist['playlist'] = currentPlaylist
                with open("/etc/enigma2/ipaudio.json", 'w')as f:
                    json.dump(playlist, f, indent=4)
                self.loadPlaylist()

    def exit(self):
        self.close()

class IPAudioInfo(Screen):
    """Info/About screen"""
    
    def __init__(self, session):
        Screen.__init__(self, session)
        
        # Select skin based on resolution and color
        if isHD():
            if config.plugins.IPAudio.skin.value == 'orange':
                self.skin = SKIN_IPAudioInfo_ORANGE_HD
            elif config.plugins.IPAudio.skin.value == 'teal':
                self.skin = SKIN_IPAudioInfo_TEAL_HD
            elif config.plugins.IPAudio.skin.value == 'lime':
                self.skin = SKIN_IPAudioInfo_LIME_HD
            else:
                self.skin = SKIN_IPAudioInfo_ORANGE_HD
        else:
            if config.plugins.IPAudio.skin.value == 'orange':
                self.skin = SKIN_IPAudioInfo_ORANGE_FHD
            elif config.plugins.IPAudio.skin.value == 'teal':
                self.skin = SKIN_IPAudioInfo_TEAL_FHD
            elif config.plugins.IPAudio.skin.value == 'lime':
                self.skin = SKIN_IPAudioInfo_LIME_FHD
            else:
                self.skin = SKIN_IPAudioInfo_ORANGE_FHD
        
        self.skinName = "IPAudioInfo"
        
        self["info_text"] = Label()
        self["key_red"] = Button(_("Close"))
        
        self["actions"] = ActionMap(["ColorActions", "OkCancelActions"],
            {
                "cancel": self.close,
                "red": self.close,
                "ok": self.close,
            }, -1)
        
        self.onLayoutFinish.append(self.showInfo)
    
    def showInfo(self):
        """Display plugin information"""
        info = """
IPAudio v{}

Original Developer
ZIKO

Maintainer
popking159

Enjoy FREE Enigma2 world!


Press OK or RED to close
        """.format(Ver)
        
        self["info_text"].setText(info.strip())

class IPAudioHelp(Screen):
    """Help screen with scrollable content"""
    
    def __init__(self, session):
        Screen.__init__(self, session)
        
        # Select skin based on resolution and color
        if isHD():
            if config.plugins.IPAudio.skin.value == 'orange':
                self.skin = SKIN_IPAudioHelp_ORANGE_HD
            elif config.plugins.IPAudio.skin.value == 'teal':
                self.skin = SKIN_IPAudioHelp_TEAL_HD
            elif config.plugins.IPAudio.skin.value == 'lime':
                self.skin = SKIN_IPAudioHelp_LIME_HD
            else:
                self.skin = SKIN_IPAudioHelp_ORANGE_HD
        else:
            if config.plugins.IPAudio.skin.value == 'orange':
                self.skin = SKIN_IPAudioHelp_ORANGE_FHD
            elif config.plugins.IPAudio.skin.value == 'teal':
                self.skin = SKIN_IPAudioHelp_TEAL_FHD
            elif config.plugins.IPAudio.skin.value == 'lime':
                self.skin = SKIN_IPAudioHelp_LIME_FHD
            else:
                self.skin = SKIN_IPAudioHelp_ORANGE_FHD
        
        self.skinName = "IPAudioHelp"
        
        from Components.Sources.List import List
        self.help_lines = []
        self["help_text"] = List(self.help_lines)
        self["key_red"] = Button(_("Close"))
        
        self["actions"] = ActionMap(["ColorActions", "OkCancelActions", "DirectionActions"],
            {
                "cancel": self.close,
                "red": self.close,
                "ok": self.close,
                "up": self.scrollUp,
                "down": self.scrollDown,
            }, -1)
        
        self.onLayoutFinish.append(self.showHelp)
    
    def showHelp(self):
        """Display help instructions as scrollable list"""
        help_lines = [
            "BASIC CONTROLS:",
            "• OK: Play selected channel",
            "• LEFT/RIGHT: Switch between categories",
            "• UP/DOWN: Navigate channel list",
            "• EXIT: Close plugin (audio continues)",
            "",
            "AUDIO CONTROLS:",
            "• GREEN: Reset/Stop audio",
            "• 7: Decrease Audio delay (-0.5s)",
            "• 9: Increase Audio delay (+0.5s)",
            "• 8: Reset Audio delay",
            "  - Sync audio with video",
            "  - Range: -10s to +10s",
            "",
            "VIDEO SYNC:",
            "• PAUSE: Activate TimeShift delay",
            "• CH+: Increase Video delay (+0.5s)",
            "• CH-: Decrease Video delay (-0.5s)",
            "  - Sync live TV with audio stream",
            "  - Range: 0 to +50s",
            "",
            "SETTINGS (MENU):",
            "• Change skin color (Orange/Teal/Lime)",
            "• Select player (GStreamer/FFmpeg)",
            "• Configure audio output",
            "• Enable/disable updates",
            "• Adjust volume level",
            "",
            "WEB INTERFACE:",
            "• Access: http://box-ip:8080/ipaudio",
            "• Manage playlists",
            "• Create categories",
            "• Drag-and-drop channels",
            "• Add/edit/delete channels",
            "",
            "BUTTONS:",
            "• RED: Exit plugin",
            "• GREEN: Reset audio",
            "• YELLOW: Show this help",
            "• BLUE: About/Info",
            "",
            "PLAYLIST MANAGEMENT:",
            "• Create unlimited categories",
            "• Each category has separate JSON file",
            "• Files in: /etc/enigma2/ipaudio/",
            "• Format: ipaudio_<name>.json",
            "",
            "TIPS:",
            "• Use audio delay for stream sync",
            "• Use TimeShift for live TV sync",
            "• Playlists auto-reload on change",
            "• Web interface updates in real-time",
            "",
            "Press UP/DOWN to scroll",
            "Press RED or EXIT to close",
        ]
        
        # Convert to list format
        self.help_lines = [(line,) for line in help_lines]
        self["help_text"].setList(self.help_lines)
    
    def scrollUp(self):
        """Scroll help text up"""
        self["help_text"].up()
    
    def scrollDown(self):
        """Scroll help text down"""
        self["help_text"].down()

class IPAudioHandler(Screen):
    container = eConsoleAppContainer()
    
    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        
        # Track service events including channel changes
        ServiceEventTracker(screen=self, eventmap={
            iPlayableService.evEnd: self.evEnd,
            iPlayableService.evStopped: self.evEnd,
            iPlayableService.evStart: self.evServiceChanged,  # Detects channel change
        })
    
    def stopIPAudio(self):
        """Stop IPAudio playback"""
        cprint("[IPAudio] stopIPAudio called")
        if self.container.running():
            self.container.kill()
    
    def evServiceChanged(self):
        """Called when service changes (channel zap) - restore audio AND video"""
        cprint("[IPAudio] Service changed - stopping external audio and restoring original")
        
        # Stop external audio when user changes channel
        if config.plugins.IPAudio.running.value:
            cprint("[IPAudio] Channel changed - restoring original audio/video")
            
            # Kill container processes
            if self.container.running():
                self.container.kill()
            
            # Kill any running audio processes
            os.system("killall -9 gst-launch-1.0 ffmpeg 2>/dev/null")
            
            # For mutable boxes - restore audio device
            if fileExists("/dev/dvb/adapter0/audio10"):
                try:
                    os.rename("/dev/dvb/adapter0/audio10", "/dev/dvb/adapter0/audio0")
                    cprint("[IPAudio] Audio device restored")
                except:
                    pass
            
            # Restart the current service to restore both audio AND video
            current_service = self.session.nav.getCurrentlyPlayingServiceReference()
            if current_service:
                cprint("[IPAudio] Restarting service to restore audio/video")
                self.session.nav.stopService()
                
                # Use timer to restart service after short delay
                from enigma import eTimer
                self.restoreTimer = eTimer()
                try:
                    self.restoreTimer.callback.append(lambda: self.restoreService(current_service))
                except:
                    self.restoreTimer_conn = self.restoreTimer.timeout.connect(lambda: self.restoreService(current_service))
                self.restoreTimer.start(100, True)  # 100ms delay
            
            # Update running status
            config.plugins.IPAudio.running.value = False
            config.plugins.IPAudio.running.save()
            
            # Unmute if using ALSA
            if HAVE_EALSA:
                try:
                    alsa = eAlsaOutput.getInstance()
                    alsa.setMute(False)
                    cprint("[IPAudio] ALSA unmuted")
                except:
                    pass
    
    def restoreService(self, service_ref):
        """Restore the service after stopping external audio"""
        cprint("[IPAudio] Restoring service: {}".format(service_ref.toString()))
        self.session.nav.playService(service_ref)
    
    def evEnd(self):
        """Called when service ends or stops"""
        cprint("[IPAudio] Service ended")
        
        # Only clean up if we were playing external audio
        if config.plugins.IPAudio.running.value:
            if not config.plugins.IPAudio.keepaudio.value:
                cprint("[IPAudio] Cleaning up audio on service end")
                self.stopIPAudio()
                os.system("killall -9 gst-launch-1.0 ffmpeg 2>/dev/null")
                
                # Restore audio device for mutable boxes
                if fileExists("/dev/dvb/adapter0/audio10"):
                    try:
                        os.rename("/dev/dvb/adapter0/audio10", "/dev/dvb/adapter0/audio0")
                    except:
                        pass
                
                config.plugins.IPAudio.running.value = False
                config.plugins.IPAudio.running.save()

class IPAudioLauncher():

    def __init__(self, session):
        self.session = session

    def gotSession(self):
        keymap = resolveFilename(SCOPE_PLUGINS, "Extensions/IPAudio/keymap.xml")
        readKeymap(keymap)
        globalActionMap.actions['IPAudioSelection'] = self.ShowHide

    def ShowHide(self):
        if not isinstance(self.session.current_dialog, IPAudioScreen):
            self.session.open(IPAudioScreen)


# Add at the end of the file, in sessionstart() function:

def sessionstart(reason, session=None, **kwargs):
    if reason == 0:
        IPAudioHandler(session)
        IPAudioLauncher(session).gotSession()
        
        # Start web interface
        try:
            from Plugins.Extensions.IPAudio.webif import startWebInterface
            from twisted.internet import reactor
            
            # Use callLater to ensure reactor is running
            reactor.callLater(2, startWebInterface)
        except Exception as e:
            print("[IPAudio] Could not start web interface: {}".format(e))
            import traceback
            traceback.print_exc()

def main(session, **kwargs):
    session.open(IPAudioScreen)


def showInmenu(menuid, **kwargs):
    if menuid == "mainmenu":
        return [("IPAudio", main, "IPAudio", 1)]
    else:
        return []


def Plugins(**kwargs):
    Descriptors = []
    Descriptors.append(PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionstart))
    if config.plugins.IPAudio.mainmenu.value:
        Descriptors.append(PluginDescriptor(where=[PluginDescriptor.WHERE_MENU], fnc=showInmenu))
    Descriptors.append(PluginDescriptor(name="IPAudio", description="Listen to your favorite commentators", icon="logo.png", where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main))
    return Descriptors
