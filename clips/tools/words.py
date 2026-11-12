import json, sys
m = json.load(open(f'/home/user/work/clips/raw_{sys.argv[1]}.words.json')); o = m['offset']
a = float(sys.argv[2]) if len(sys.argv) > 2 else 0; b = float(sys.argv[3]) if len(sys.argv) > 3 else 1e9
line = ''; t = None; prev = None
for w in m['words']:
    s = o + w['s']
    if not (a <= s <= b): continue
    if prev is not None and s - prev > 1.5: line += f' [gap {s-prev:.0f}s]'
    if t is None: t = s
    line += w['w']; prev = o + w['e']
    if len(line) > 100: print(f'{t:8.1f}', line); line = ''; t = None
if line: print(f'{t:8.1f}', line)
