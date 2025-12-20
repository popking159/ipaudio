# gst_wrapper.py

from Tools.Directories import fileExists
from Components.config import config
from Plugins.Extensions.IPAudio.alsa_helper import detect_alsa_device

REDC = "**"
ENDC = "**"

def cprint(text):
    print(REDC + text + ENDC)


def clamp(value, minv, maxv):
    return max(minv, min(maxv, value))


def get_gst_eq_filter():
    """Return GStreamer equalizer filter string or None."""
    eq = config.plugins.IPAudio.equalizer.value

    presets_3band = {
        "bass_boost":  "equalizer-3bands band0=-6.0 band1=-3.0 band2=6.0",
        "treble_boost":"equalizer-3bands band0=6.0 band1=-3.0 band2=-6.0",
        "vocal":       "equalizer-3bands band0=-3.0 band1=6.0 band2=-3.0",
        "rock":        "equalizer-3bands band0=5.0 band1=3.0 band2=-2.0",
        "pop":         "equalizer-3bands band0=-2.0 band1=5.0 band2=3.0",
        "classical":   "equalizer-3bands band0=4.0 band1=0.0 band2=-4.0",
        "jazz":        "equalizer-3bands band0=3.0 band1=2.0 band2=4.0",
    }

    if eq == "off":
        return None
    return presets_3band.get(eq)


def get_gst_sink():
    """
    Map IPAudio 'sync' setting to actual sink element.
    For alsasink, use detected ALSA device where meaningful.
    """
    val = config.plugins.IPAudio.sync.value  # "alsasink", "osssink", "autoaudiosink", ...
    if val == "alsasink":
        dev = detect_alsa_device()
        if dev == "default":
            return "alsasink"              # let asound.conf route default
        else:
            return 'alsasink device="{}"'.format(dev)
    elif val == "osssink":
        return "osssink"
    else:
        return "autoaudiosink"


def build_gst_cmd(url, delay_sec=0, volume_level=None):
    """
    Build gst-launch-1.0 pipeline for IPAudio:
      uridecodebin -> audioconvert -> audioresample -> volume -> [eq] -> [delay] -> sink.
    """
    if not url:
        raise ValueError("Empty URL passed to build_gst_cmd")

    cmd = (
        'gst-launch-1.0 -e '
        'uridecodebin uri="{url}" ! '
        'audioconvert ! audioresample ! audio/x-raw,rate=48000 ! '
    ).format(url=url)

    vol_raw = volume_level if volume_level is not None else config.plugins.IPAudio.volLevel.value
    volume = vol_raw / 10.0
    cmd += 'volume volume={} ! '.format(volume)

    eq_filter = get_gst_eq_filter()
    if eq_filter:
        cmd += '{} ! '.format(eq_filter)

    # Delay using queue max-size-time (positive only)
    delay_ms = int(delay_sec * 1000) if delay_sec is not None else 0
    if delay_ms > 0:
        delay_ms = clamp(delay_ms, 0, 60000)  # safety: max 60s
        delay_ns = delay_ms * 1000000
        cmd += 'queue max-size-time={} ! '.format(delay_ns)

    sink = get_gst_sink()
    # match your working cmd: sync=false provide-clock=false
    cmd += '{} sync=false provide-clock=false'.format(sink)

    cprint("[IPAudio] GStreamer command: {}".format(cmd))
    cprint("[IPAudio] Volume level: {} = {}x".format(vol_raw, volume))
    return cmd
