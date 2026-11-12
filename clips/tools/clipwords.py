import json, glob, os, subprocess, torch, whisper
torch.set_num_threads(4)
m = whisper.load_model("small.en")
for ts in sorted(glob.glob("/home/user/work/clips/raw_*.ts")):
    out = ts.replace(".ts", ".words.json")
    if os.path.exists(out): continue
    off = json.load(open(ts.replace(".ts", ".json")))["offset"]
    wav = ts.replace(".ts", ".wav")
    subprocess.check_call(["ffmpeg","-loglevel","error","-y","-i",ts,"-ac","1","-ar","16000",wav])
    r = m.transcribe(wav, language="en", word_timestamps=True, fp16=False, condition_on_previous_text=False)
    words = [{"w": w["word"], "s": round(w["start"],2), "e": round(w["end"],2)} for s in r["segments"] for w in s["words"]]
    json.dump({"offset": off, "words": words}, open(out, "w"))
    print("done", ts, flush=True)
