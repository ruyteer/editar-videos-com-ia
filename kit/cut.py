"""Corta os trechos de keep.json, acelera a fala, entrega 1080x1920 e trata o áudio.

keep.json = lista de [inicio, fim] em segundos do vídeo original, na ordem final. Ex.: [[0.8,4.5],[6.3,9.6]]

Uso:
  python cut.py src.mp4 keep.json tight.mp4 [--speed 1.07] [--crop 423:752:30:0] [--boost 0]

--crop  recorte ffmpeg (w:h:x:y) quando o vídeo não é 9:16 (aplicado antes do scale)
--boost dB extras para voz baixa (ex.: 10)
"""
import argparse, json, subprocess, os, tempfile

p = argparse.ArgumentParser()
p.add_argument("src"); p.add_argument("keep"); p.add_argument("out")
p.add_argument("--speed", type=float, default=1.07)
p.add_argument("--crop", default="")
p.add_argument("--boost", type=float, default=0)
a = p.parse_args()

keep = json.load(open(a.keep))
parts = []
for i, (s, e) in enumerate(keep):
    d = e - s
    parts.append(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS[v{i}];"
                 f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={d-0.012:.3f}:d=0.012[a{i}]")
n = len(keep)
crop = f"crop={a.crop}," if a.crop else ""
fc = ";".join(parts) + ";" + "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca];"
fc += (f"[cv]setpts=PTS/{a.speed},{crop}scale=1080:1920:flags=lanczos,unsharp=5:5:0.5,"
       f"eq=contrast=1.05:saturation=0.98,fps=30,format=yuv420p[vo];")
fc += (f"[ca]atempo={a.speed},highpass=f=80,afftdn=nf=-30,volume={a.boost}dB,"
       f"acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,alimiter=limit=0.9[ao]")
fcfile = os.path.join(tempfile.gettempdir(), "_cut_fc.txt")
open(fcfile, "w").write(fc)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.src, "-/filter_complex", fcfile, "-map", "[vo]", "-map", "[ao]",
                "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-g", "30", "-keyint_min", "30", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.out], check=True)
print(f"ok -> {a.out}  (~{sum(e - s for s, e in keep) / a.speed:.1f}s)")
