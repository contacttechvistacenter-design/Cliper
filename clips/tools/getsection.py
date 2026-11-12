"""Download a time range of the Twitch VOD by fetching HLS segments through the proxy.
usage: VOD_URL=<twitch vod url> getsection.py START_SEC END_SEC OUT.ts [format]
Output starts exactly at the first segment boundary <= START; prints that offset."""
import os, subprocess, sys, json, tempfile, urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = os.environ.get("VOD_URL", "https://www.twitch.tv/videos/2921253522")  # set VOD_URL for another VOD
YTDLP = "/home/user/Cliper/backend/.venv/bin/yt-dlp"
start, end, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
fmt = sys.argv[4] if len(sys.argv) > 4 else "1080p60"
cache = f"/home/user/work/m3u8_{URL.rstrip('/').split('/')[-1]}_{fmt}.url"
if os.path.exists(cache):
    m3u8 = open(cache).read().strip()
else:
    m3u8 = subprocess.check_output([YTDLP, "--no-warnings", "-f", fmt, "-g", URL], text=True).strip()
    open(cache, "w").write(m3u8)
base = m3u8.rsplit("/", 1)[0]
lines = urllib.request.urlopen(m3u8).read().decode().splitlines()
segs, t, dur = [], 0.0, None
for ln in lines:
    if ln.startswith("#EXTINF:"):
        dur = float(ln.split(":")[1].rstrip(","))
    elif ln and not ln.startswith("#"):
        segs.append((t, dur, ln)); t += dur
need = [s for s in segs if s[0] + s[1] > start and s[0] < end]
tmp = tempfile.mkdtemp(dir="/home/user/work")
def fetch(i_s):
    i, (_, _, name) = i_s
    p = f"{tmp}/{i:05d}.ts"
    for _ in range(4):
        try:
            data = urllib.request.urlopen(f"{base}/{name}", timeout=60).read()
            open(p, "wb").write(data); return p
        except Exception:
            name = name.replace(".ts", "-muted.ts") if "-muted" not in name else name.replace("-muted", "")
    raise RuntimeError(name)
with ThreadPoolExecutor(8) as ex:
    parts = list(ex.map(fetch, enumerate(need)))
lst = f"{tmp}/list.txt"
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.check_call(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out])
subprocess.call(["rm", "-rf", tmp])
print(json.dumps({"offset": need[0][0], "out": out}))
