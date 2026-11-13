"""9:16 (1080x1920) clip: hook / video strip / [watermark] / captions / thumbnail or face cam.
usage: render_clip.py CONFIG.json OUT.mp4  (config example: clips/juancar/perro_01.json; run from the repo root)

Layout: blurred copy of the video as background; hook text on top; video strip
(source UI cropped out); optional watermark under it; captions in their own band; then the
thumbnail (Juancar campaign) or a face-cam card (cam in the config, streamer clips).
Config keys: src, hook, ranges, cues; optional thumb, logo, vid, vid_out, cam, cam_out, hook_y, cap_y, fps.
"""
import json, subprocess, sys

CFG = json.load(open(sys.argv[1]))
SRC, HOOK = CFG["src"], CFG["hook"]
THUMB, LOGO = CFG.get("thumb"), CFG.get("logo")   # both optional
VID, VID_OUT = CFG.get("vid", [1160, 483, 60, 60]), CFG.get("vid_out", [1080, 450, 395])  # vid: source crop [w,h,x,y]; vid_out: [w,h,y]
CAM, CAM_OUT = CFG.get("cam"), CFG.get("cam_out", [880, 495, 1150])    # optional face cam: crop [x,y,w,h]; out [w,h,y]
HOOK_Y, CAP_Y, FPS = CFG.get("hook_y", 285), CFG.get("cap_y", 1000), CFG.get("fps", 30)
THUMB_Y, LOGO_Y = CFG.get("thumb_y", 1070), CFG.get("logo_y", 858)
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
            events.append(f"Dialogue: 1,{ts(s)},{ts(end)},Cap,,0,0,0,,{{\\an5\\pos(540,{CAP_Y})}}{line}")

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
Dialogue: 2,{ts(0)},{ts(dur)},Hook,,0,0,0,,{{\\an5\\pos(540,{HOOK_Y})}}{HOOK}
""" + "\n".join(events) + "\n"
open(f"{D}/clip.ass", "w").write(ass)

inputs = []
for a, b in RANGES:
    inputs += ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", SRC]
n = len(RANGES)
extra, idx = [], n
for img in (THUMB, LOGO):
    if img: extra += ["-loop", "1", "-i", img]
ns = 3 if CAM else 2
fc = ("".join(f"[{i}:v][{i}:a]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca];"
      f"[cv]split={ns}" + "".join(f"[c{i + 1}]" for i in range(ns)) + ";"
      "[c1]scale=-2:1920,crop=1080:1920,boxblur=40:6,eq=brightness=-0.25[bg];"
      f"[c2]crop={VID[0]}:{VID[1]}:{VID[2]}:{VID[3]},scale={VID_OUT[0]}:{VID_OUT[1]}[vid];")
cur, steps = "bg", [("vid", f"(W-w)/2:{VID_OUT[2]}")]
if CAM:
    fc += f"[c3]crop={CAM[2]}:{CAM[3]}:{CAM[0]}:{CAM[1]},scale={CAM_OUT[0]}:{CAM_OUT[1]},unsharp=5:5:0.6[camv];"
    steps.append(("camv", f"(W-w)/2:{CAM_OUT[2]}"))
if THUMB:
    fc += f"[{idx}:v]scale=1080:608[thumb];"; idx += 1; steps.append(("thumb", f"0:{THUMB_Y}"))
if LOGO:
    fc += f"[{idx}:v]crop=1840:275:40:205,scale=560:-1[logo];"; idx += 1; steps.append(("logo", f"(W-w)/2:{LOGO_Y}"))
for i, (lab, pos) in enumerate(steps):
    fc += f"[{cur}][{lab}]overlay={pos}[t{i}];"; cur = f"t{i}"
fc += f"[{cur}]ass={D}/clip.ass:fontsdir={FONTS},format=yuv420p[v];[ca]loudnorm=I=-14:TP=-1.5:LRA=11[a]"
subprocess.check_call(["ffmpeg", "-loglevel", "error", "-y", *inputs, *extra,
                       "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{dur:.2f}", "-r", str(FPS),
                       "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                       "-movflags", "+faststart", out])
print(out, f"{dur:.1f}s")
