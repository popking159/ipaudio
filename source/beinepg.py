# beinepg.py (inside Plugins/Extensions/IPAudio)
import json, os
from datetime import datetime, timedelta, timezone
from Components.config import config
import urllib.request
import json
import os
from .plugin import getPlaylistDir  # you already have this helper

TMP_JSON = "/var/volatile/tmp/beinepg.json"

def get_simple_epg_path():
    return os.path.join(config.plugins.IPAudio.settingsPath.value, "simple_epg.json")

DEBUG_LOG = "/tmp/IPAudio_bein_url.log"

def log_debug(text):
    try:
        with open(DEBUG_LOG, "a") as f:
            f.write(text + "\n")
    except:
        pass

def build_url():
    base = "https://www.beinsports.com/api/opta/tv-event"

    channel_params = (
        "&channelIds=7836FEA9-6B39-4A1A-8352-DC5FCB97A16C"
        "&channelIds=FD1DD7DD-1E7B-4AA2-8682-BFA17338E653"
        "&channelIds=8AEA2426-D451-4BA5-BF48-114A1F04B1A8"
        "&channelIds=DB9361E8-B3EB-4D6F-9A82-75B5F09E2F92"
        "&channelIds=964E6246-CA95-410B-82C4-EA75DD979435"
        "&channelIds=E24D9C11-A8B4-4C7F-AD3E-B3364FB6D5A2"
        "&channelIds=A892063B-A5D9-4199-95AC-6A214515FA6B"
        "&channelIds=0F8D20A4-D46C-4B18-9242-8E7B3E978FF8"
        "&channelIds=5C08D9D3-C713-4F1F-947E-87C761428B9B"
        "&channelIds=7B558284-F996-4123-9584-1E5D01844270"
        "&channelIds=84F7E0C1-D47A-4444-BBA8-C50BB8D2C5A8"
        "&channelIds=67DD49E9-E3A2-4B3A-94B8-88C620A4DFB1"
        "&channelIds=E3B37FA0-E582-45B2-BB8E-516E1A714EF6"
        "&channelIds=27E67022-B943-4913-9AF3-AFD3DAC9854B"
        "&channelIds=CDF1A4C8-26DD-4C33-A239-F729A3B09295"
        "&channelIds=7A8040D9-7BAF-477E-B9F7-8BAB88F677E8"
        "&channelIds=51D28C47-7B79-4007-81A3-BFDF9BC65A3B"
        "&channelIds=9ABD32F9-C6D9-4DD5-B936-2C7E6546292E"
        "&channelIds=1752F091-A114-4629-BED4-46E0BB488A24"
        "&channelIds=CD634732-20D1-4137-94E7-939DE93D056D"
        "&channelIds=522050CE-EBD3-43EA-B636-42B034FDC05C"
        "&channelIds=8C1EC4FC-35E6-4866-A75D-37FCFAE18839"
        "&channelIds=846C79D6-18F8-4A4D-ACFA-2C18DCCB6398"
        "&channelIds=2F518547-2269-4C07-93D5-2733397472BD"
        "&channelIds=93000494-0DF8-4107-AF0E-1C99D3DBB2EC"
        "&channelIds=9B969275-E59C-4DD1-8FCA-8B01EAE04909"
        "&channelIds=2FB43094-3598-43C1-A3BA-44BFB40092E0"
        "&channelIds=008F0EA9-FCD9-4E8C-849A-913979E7450A"
        "&channelIds=7783DC02-4527-4094-9EE3-CDA8E093E4EB"
        "&channelIds=5B15611A-5F9D-4EF0-89A6-677C9CA2BD5D"
        "&channelIds=F7215920-CCF9-4DBB-8B9D-152E232FA549"
        "&channelIds=DC04009D-7E18-4D1C-BA7F-7269B8F8D065"
    )

    now_utc = datetime.now(timezone.utc)

    # Window: from today 10:00Z to tomorrow 09:59:59.999Z
    start = now_utc.replace(hour=10, minute=0, second=0, microsecond=0)
    # If current time is before 10:00, move window to yesterday→today
    if now_utc < start:
        start -= timedelta(days=1)
    end = start + timedelta(days=1) - timedelta(milliseconds=1)

    def fmt(dt):
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    endAfter_str = fmt(start)  # start of window
    startBefore_str = fmt(end) # end of window

    def encode_colons(s):
        return s.replace(":", "%3A")

    startBefore_param = "startBefore={}".format(encode_colons(startBefore_str))
    endAfter_param = "endAfter={}".format(encode_colons(endAfter_str))

    url = "{}?searchKey=&{}&{}&limit=3000{}".format(
        base, startBefore_param, endAfter_param, channel_params
    )

    log_debug("[beIN] Built URL: {}".format(url))
    return url

def fetch_and_build_simple_epg():
    url = build_url()
    log_debug("[beIN] Fetching URL: {}".format(url))

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
        }
    )

    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode("utf-8"))

    with open(TMP_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    events = []

    # Read user‑configured offset relative to UTC+03:00
    offset_rel = int(config.plugins.IPAudio.epgOffset.value)
    offset = timedelta(hours=offset_rel)

    for row in data.get("rows", []):
        event_data = row.get("data", {})
        channel_name = event_data.get("ChannelName", "")
        title = event_data.get("Title", {}).get("English", "Unknown Event")
        desc = event_data.get("Synopsis", {}).get("English", "")

        start_time_str = event_data.get("StartTime", "")
        end_time_str = event_data.get("EndTime", "")

        try:
            dt_start = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
            dt_end = datetime.fromisoformat(end_time_str.replace("Z", "+00:00"))
        except Exception:
            continue

        # Apply your desired shift
        local_start = dt_start + offset
        local_end = dt_end + offset

        events.append({
            "channel": channel_name,
            "title": title,
            "desc": desc,
            "start": local_start.strftime("%H:%M"),
            "end": local_end.strftime("%H:%M"),
            "start_full": local_start.strftime("%Y%m%d%H%M%S"),
            "end_full": local_end.strftime("%Y%m%d%H%M%S"),
        })

    simple_epg = {"events": events}

    out_path = get_simple_epg_path()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(simple_epg, f, ensure_ascii=False, indent=2)

    return out_path

