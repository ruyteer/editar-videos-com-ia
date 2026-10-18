#!/bin/bash
# Mix dos efeitos + loudness em 2 passadas (-14 LUFS, pico -2 dBTP) + verificação.
# Uso: ./finish.sh master.mp4 cues.json 2.8 final.mp4
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
python "$DIR/mix.py" "$1" "$2" mix.mkv "$3"
M=$(ffmpeg -hide_banner -i mix.mkv -af loudnorm=I=-14:TP=-2:LRA=11:print_format=json -f null - 2>&1 | python -c "
import sys,json;t=sys.stdin.read();a=t.rindex('{');b=t.index('}',a);d=json.loads(t[a:b+1])
print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -v error -y -i mix.mkv -c:v copy -af "loudnorm=I=-14:TP=-2:LRA=11:$M:linear=true,aresample=48000" \
  -c:a aac -b:a 192k -movflags +faststart "$4"
echo "Loudness final:"
ffmpeg -hide_banner -i "$4" -af loudnorm=I=-14:TP=-2:print_format=json -f null - 2>&1 | grep -E '"input_(i|tp)"'
echo "Confira que os efeitos estão audíveis (pico sobe nos cues):"
python - "$1" "$2" <<'EOF'
import json, re, subprocess, sys
m, cues = sys.argv[1], json.load(open(sys.argv[2]))
def mx(f, t):
    r = subprocess.run(["ffmpeg","-hide_banner","-ss",str(t),"-t","0.5","-i",f,"-vn","-af","volumedetect","-f","null","-"],capture_output=True,text=True)
    g = re.search(r"max_volume: (-?[\d.]+)", r.stderr); return float(g.group(1)) if g else -99
for t, n, _ in cues[:: max(1, len(cues)//6)]:
    print(f"  {t:6.2f}s {n:9s} sem sfx {mx(m,t):6.1f} dB | com sfx {mx('mix.mkv',t):6.1f} dB")
EOF
