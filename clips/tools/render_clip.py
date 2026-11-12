"""9:16 (1080x1920) promo clip: hook / video / channel watermark / captions / thumbnail.
usage: render_clip.py CONFIG.json OUT.mp4  (config example: clips/juancar/perro_01.json; run from the repo root)

Layout: blurred copy of the video as background; hook text on top; video strip
(clock, burned-in subs and Twitch logos cropped out); YouTube watermark under it;
our Spanish captions (the source subs only show ~15% of the time); thumbnail at the bottom.
"""
import json, subprocess, sys

CFG = json.load(open(sys.argv[1]))
SRC, THUMB, LOGO, HOOK = CFG["src"], CFG["thumb"], CFG["logo"], CFG["hook"]
FONTS = CFG.get("fonts", "backend/fonts")
RANGES = [tuple(r) for r in CFG["ranges"]]   # kept source ranges, in order (seconds)
CUES = [tuple(c) for c in CFG["cues"]]       # (start, end, text) in source seconds
D = CFG.get("workdir", "/tmp")
out = sys.argv[2]

def remap(t):
    acc = 0.0
    for a, b in RANGES:
        if a - 0.01 <= t <= b + 0.01:
            return acc + max(0.0, t - a)
        acc += b - a
    return None
dur = sum(b - a for a, b in RANGES)

def ts(t):
    t = max(0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"

# word times: split each cue over its words by character length
YEL, WHT = r"{\c&H0000E5FF&}", r"{\c&H00FFFFFF&}"
events = []
for a, b, text in CUES:
    ws = text.split()
    tot = sum(len(w) + 1 for w in ws)
    t, words = remap(a), []
    for w in ws:
        d = (b - a) * (len(w) + 1) / tot
        words.append((w.upper(), t, t + d)); t += d
    for i in range(0, len(words), 3):
        g = words[i:i + 3]
        for j, (w, s, e) in enumerate(g):
            end = g[j + 1][1] if j + 1 < len(g) else g[-1][2]
            line = " ".join((YEL if k == j else WHT) + x[0] for k, x in enumerate(g))
            events.append(f"Dialogue: 1,{ts(s)},{ts(end)},Cap,,0,0,0,,{{\\an5\\pos(540,1000)}}{line}")

ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,TikTok Sans,76,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,3,5,40,40,0,1
Style: Hook,TikTok Sans,78,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,1,0,0,0,100,100,0,0,3,20,0,5,50,50,0,1

[Events]
Dialogue: 2,{ts(0)},{ts(dur)},Hook,,0,0,0,,{{\\an5\\pos(540,215)}}{HOOK}
""" + "\n".join(events) + "\n"
open(f"{D}/clip.ass", "w").write(ass)

inputs = []
for a, b in RANGES:
    inputs += ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", SRC]
n = len(RANGES)
fc = ("".join(f"[{i}:v][{i}:a]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca];"
      "[cv]split=2[c1][c2];"
      "[c1]scale=-2:1920,crop=1080:1920,boxblur=40:6,eq=brightness=-0.25[bg];"
      "[c2]crop=1160:525:60:60,scale=1080:489[vid];"
      f"[{n}:v]scale=1080:608[thumb];"
      f"[{n+1}:v]crop=1840:275:40:205,scale=560:-1[logo];"
      "[bg][vid]overlay=0:330[t1];[t1][logo]overlay=(W-w)/2:838[t2];[t2][thumb]overlay=0:1085[t3];"
      f"[t3]ass={D}/clip.ass:fontsdir={FONTS},format=yuv420p[v];"
      "[ca]loudnorm=I=-14:TP=-1.5:LRA=11[a]")
subprocess.check_call(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-loop", "1", "-i", THUMB, "-loop", "1", "-i", LOGO,
                       "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{dur:.2f}", "-r", "30",
                       "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                       "-movflags", "+faststart", out])
print(out, f"{dur:.1f}s")
