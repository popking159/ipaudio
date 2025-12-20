from Tools.Directories import fileExists

def detect_alsa_device():
    """
    Decide which ALSA device string to use.
    If /etc/asound.conf exists, trust 'default'.
    Fallback: hw:0,0 when card0 exists, else default.
    """
    if fileExists("/etc/asound.conf"):
        return "default"

    if fileExists("/proc/asound/card0"):
        return "hw:0,0"

    return "default"
