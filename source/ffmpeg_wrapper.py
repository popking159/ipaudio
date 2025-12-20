# ffmpeg_wrapper.py

from Tools.Directories import fileExists
from Components.config import config
from Plugins.Extensions.IPAudio.alsa_helper import detect_alsa_device

REDC = "**"
ENDC = "**"

def cprint(text):
    print(REDC + text + ENDC)


def clamp(value, minv, maxv):
    return max(minv, min(maxv, value))


def get_ffmpeg_eq_filter():
    """Return FFmpeg equalizer filter string or None."""
    eq = config.plugins.IPAudio.equalizer.value
    if eq == "off":
        return None

    presets = {
        "bass_boost": (-6.0, -3.0,  6.0),
        "treble_boost": ( 6.0, -3.0, -6.0),
        "vocal":       (-3.0,  6.0, -3.0),
        "rock":        ( 5.0,  3.0, -2.0),
        "pop":         (-2.0,  5.0,  3.0),
        "classical":   ( 4.0,  0.0, -4.0),
        "jazz":        ( 3.0,  2.0,  4.0),
    }
    gains = presets.get(eq)
    if not gains:
        return None

    g0, g1, g2 = gains
    return (
        "equalizer=f=100:t=h:width_type=o:width=1:g={g0},"
        "equalizer=f=1000:t=h:width_type=o:width=1:g={g1},"
        "equalizer=f=8000:t=h:width_type=o:width=1:g={g2}"
    ).format(g0=g0, g1=g1, g2=g2)


def get_boxtype():
    try:
        with open("/proc/stb/info/boxtype", "r") as f:
            return f.read().strip()
    except:
        return ""


def use_new_adelay_syntax():
    bt = get_boxtype()
    # Novaler models using ffmpeg 8 syntax
    return bt in ("novaler4kse", "novaler4kpro")


def build_ffmpeg_cmd(url, delay_sec=0, volume_level=None, track_index=None):
    """
    Build a complete ffmpeg command string for ALSA playback.

    delay_sec: float/int, negative (trim start), zero, or positive (adelay).
    volume_level: 1–100 from config.plugins.IPAudio.volLevel; mapped to 0.2–2.0.
    track_index: None or int (0-based) for specific audio track.
    """
    if not url:
        raise ValueError("Empty URL passed to build_ffmpeg_cmd")

    alsa_device = detect_alsa_device()

    # Input
    input_part = "-i '{}'".format(url)

    # Filters: delay, volume, equalizer
    filters = []

    if delay_sec is not None and delay_sec > 0:
        delay_sec = clamp(delay_sec, 0, 60)
        delay_ms = int(delay_sec * 1000)
        if use_new_adelay_syntax():
            filters.append("adelay=delays={0}|{0}:all=1".format(delay_ms))
        else:
            filters.append("adelay={0}|{0}".format(delay_ms))

    if volume_level is not None:
        vol_norm = clamp(int(volume_level), 1, 100)
        vol_factor = 0.2 + (vol_norm - 1) * (1.8 / 99.0)
        filters.append("volume={:.2f}".format(vol_factor))

    eq_ff = get_ffmpeg_eq_filter()
    if eq_ff:
        filters.append(eq_ff)

    if filters:
        filter_str = ",".join(filters)
        af_part = '-af "{}"'.format(filter_str)
    else:
        af_part = ""

    # Negative delay via -ss
    ss_part = ""
    if delay_sec is not None and delay_sec < 0:
        trim_sec = clamp(abs(delay_sec), 0, 60)
        ss_part = "-ss {}".format(trim_sec)

    # Track selection
    map_part = ""
    if track_index is not None and track_index >= 0:
        map_part = "-map 0:a:{}".format(int(track_index))

    parts = [
        "ffmpeg",
        ss_part,
        input_part,
        af_part,
        map_part,
        "-vn",
        "-f alsa",
        alsa_device,
    ]
    cmd = " ".join(p for p in parts if p.strip())
    cprint("IPAudio FFmpeg cmd: {}".format(cmd))
    return cmd
