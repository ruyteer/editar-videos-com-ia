"""Mixa os efeitos sonoros sobre o áudio do vídeo renderizado.

cues.json = [[tempo_s, "nome_do_sfx", ganho], ...]  (ganho base 0.12–0.30)
Uso: python mix.py master.mp4 cues.json mix.mkv [K=2.8]
K multiplica todos os ganhos (2.8 ≈ efeitos ~7 dB abaixo dos picos da voz).
"""
import json, os, subprocess, sys, tempfile

vin, cues, out = sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3]
K = float(sys.argv[4]) if len(sys.argv) > 4 else 2.8
missing = [n for _, n, _ in cues if not os.path.exists(f"sfxn/{n}.wav")]
if missing:
    raise SystemExit(f"faltam efeitos em sfxn/: {sorted(set(missing))}")
inputs = ["-i", vin]; fl = []; labels = []
for i, (t, name, g) in enumerate(cues):
    inputs += ["-i", f"sfxn/{name}.wav"]; ms = int(t * 1000)
    fl.append(f"[{i+1}:a]volume={g*K:.3f},adelay={ms}|{ms}[s{i}]"); labels.append(f"[s{i}]")
fl.append("[0:a]aresample=48000[v]")
fl.append("[v]" + "".join(labels) + f"amix=inputs={len(cues)+1}:normalize=0:duration=first[mx]")
fc = os.path.join(tempfile.gettempdir(), "_mix_fc.txt"); open(fc, "w").write(";".join(fl))
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-/filter_complex", fc, "-map", "0:v", "-map", "[mx]",
                "-c:v", "copy", "-c:a", "pcm_s16le", out], check=True)
print("ok ->", out)
