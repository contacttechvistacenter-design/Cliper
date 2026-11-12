"""Render one 9:16 clip.
usage: render.py ID "A-B,C-D" "TITLE" LAYOUT_JSON [FIXES_JSON]  (absolute VOD seconds)
LAYOUT_JSON: {"type":"split","gx":640,"fx":40,"fy":480,"fw":720}  or  {"type":"fit","x":400,"w":1160}
"""
import json, subprocess, sys

cid, title, layout = sys.argv[1], sys.argv[3], json.loads(sys.argv[4])
ranges = [tuple(float(x) for x in r.split("-")) for r in sys.argv[2].split(",")]
D = "/home/user/work/clips"
FONTS = "/home/user/Cliper/backend/fonts"
meta = json.load(open(f"{D}/raw_{cid}.words.json"))
off = meta["offset"]
rel = [(a - off, b - off) for a, b in ranges]
dur = sum(b - a for a, b in rel)
def remap(t):
    acc = 0.0
    for a, b in rel:
        if a <= t <= b: return acc + t - a
        acc += b - a
    return None

def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def clean(w):
    return w.strip().upper().replace("{", "").replace("}", "")

# words relative to clip start, inside the clip
words = []
for w in meta["words"]:
    mid = (w["s"] + w["e"]) / 2
    if remap(mid) is None or not clean(w["w"]): continue
    s_ = remap(w["s"]); e_ = remap(w["e"])
    if s_ is None: s_ = remap(mid) - 0.05
    if e_ is None: e_ = remap(mid) + 0.05
    words.append(dict(w=clean(w["w"]), s=s_, e=e_))
if len(sys.argv) > 5:  # optional manual word fixes: {"WRONG":"RIGHT"}
    fixes = json.loads(sys.argv[5])
    for k, v in [(k, v) for k, v in fixes.items() if " " in k]:  # phrase fixes
        ks = [x.strip(".,!?") for x in k.split()]; i = 0
        while i + len(ks) <= len(words):
            if [x["w"].strip(".,!?") for x in words[i:i + len(ks)]] == ks:
                words[i]["w"] = v; words[i]["e"] = words[i + len(ks) - 1]["e"]
                del words[i + 1:i + len(ks)]
            i += 1
    fixes = {k: v for k, v in fixes.items() if " " not in k}
    for w in words:
        for k, v in fixes.items():
            if w["w"].strip(".,!?") == k:
                w["w"] = w["w"].replace(k, v)

# group into short caption lines (<=3 words, break on pauses / punctuation)
groups, cur = [], []
for w in words:
    if cur and (len(cur) >= 3 or w["s"] - cur[-1]["e"] > 0.6 or cur[-1]["w"][-1:] in ".?!"):
        groups.append(cur); cur = []
    cur.append(w)
if cur: groups.append(cur)

YEL, WHT = r"{\c&H0000E5FF&}", r"{\c&H00FFFFFF&}"
events = []
for gi, g in enumerate(groups):
    g_end = g[-1]["e"]
    if gi + 1 < len(groups) and groups[gi + 1][0]["s"] - g_end < 0.4:
        g_end = groups[gi + 1][0]["s"]
    for wi, w in enumerate(g):
        st = w["s"] if wi else g[0]["s"]
        en = g[wi + 1]["s"] if wi + 1 < len(g) else g_end
        if en - st < 0.05: continue
        txt = " ".join((YEL if j == wi else WHT) + x["w"] for j, x in enumerate(g))
        events.append(f"Dialogue: 1,{ts(st)},{ts(min(en, dur))},Cap,,0,0,0,,{{\\an5\\pos(540,{layout.get('capy',1020)})}}{txt}")

title_ev = (f"Dialogue: 2,{ts(0)},{ts(min(4.5, dur))},Title,,0,0,0,,"
            f"{{\\an8\\pos(540,110)\\fad(150,300)}}{title}")

ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,TikTok Sans,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,3,5,40,40,0,1
Style: Title,TikTok Sans,66,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,1,0,0,0,100,100,0,0,3,18,0,8,70,70,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
{title_ev}
""" + "\n".join(events) + "\n"
open(f"{D}/clip_{cid}.ass", "w").write(ass)

if layout["type"] == "split":
    gx, gy = layout.get("gx", 640), layout.get("gy", 0)
    gh = layout.get("gh", 1080); gw = round(gh * 1080 / 1020)
    fx, fy, fw = layout.get("fx", 40), layout.get("fy", 480), layout.get("fw", 720)
    fh = round(fw * 900 / 1080)
    vf = (f"[0:v]split=2[a][b];[a]crop={gw}:{gh}:{gx}:{gy},scale=1080:1020[top];"
          f"[b]crop={fw}:{fh}:{fx}:{fy},scale=1080:900[bot];[top][bot]vstack[v0]")
else:
    x, w = layout["x"], layout["w"]
    h = layout.get("h", 1080); y = layout.get("y", 0)
    vf = (f"[0:v]split=2[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=30:5,eq=brightness=-0.15[bg];"
          f"[b]crop={w}:{h}:{x}:{y},scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2[v0]")
n = len(rel)
cat = "".join(f"[{i}:v][{i}:a]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca];"
vf = cat + vf.replace("[0:v]", "[cv]").replace("[v0]", "[vs]")
vf += f";[ca]loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
vf += f";[vs]ass={D}/clip_{cid}.ass:fontsdir={FONTS},format=yuv420p[v]"

out = f"/home/user/Cliper/clips/speed_{cid}.mp4"
inputs = []
for a, b in rel:
    inputs += ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", f"{D}/raw_{cid}.ts"]
subprocess.check_call(["ffmpeg", "-loglevel", "error", "-y", *inputs,
                       "-filter_complex", vf, "-map", "[v]", "-map", "[aout]",
                       "-r", "60", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                       "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
                       "-movflags", "+faststart", out])
print(out, f"{dur:.1f}s", len(events), "caption events")
