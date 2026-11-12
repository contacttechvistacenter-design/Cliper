import json, os, sys, time
import numpy as np
import torch
import whisper

torch.set_num_threads(1)
WAV = "/home/user/work/audio16k.wav"
OUT = "/home/user/work/transcript"
os.makedirs(OUT, exist_ok=True)
CHUNK = 600  # seconds
SR = 16000

audio = whisper.load_audio(WAV)
total = len(audio) / SR
model = whisper.load_model(sys.argv[1] if len(sys.argv) > 1 else "base.en")
n = int(np.ceil(total / CHUNK))
W, K = int(sys.argv[2]), int(sys.argv[3])
for i in range(n):
    if i % K != W:
        continue
    path = f"{OUT}/chunk_{i:03d}.json"
    if os.path.exists(path):
        continue
    t0 = time.time()
    seg_audio = audio[i * CHUNK * SR:(i + 1) * CHUNK * SR]
    res = model.transcribe(seg_audio, language="en", word_timestamps=True,
                           condition_on_previous_text=False, fp16=False)
    off = i * CHUNK
    segs = []
    for s in res["segments"]:
        segs.append({
            "start": round(s["start"] + off, 2), "end": round(s["end"] + off, 2),
            "text": s["text"].strip(),
            "words": [{"w": w["word"], "s": round(w["start"] + off, 2), "e": round(w["end"] + off, 2)}
                      for w in s.get("words", [])],
        })
    with open(path, "w") as f:
        json.dump(segs, f)
    print(f"chunk {i+1}/{n} done in {time.time()-t0:.0f}s", flush=True)
print("ALL DONE", flush=True)
