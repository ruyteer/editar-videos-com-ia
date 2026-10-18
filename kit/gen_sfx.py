"""Gera e normaliza efeitos sonoros na ElevenLabs.

Requer a variável de ambiente ELEVENLABS_API_KEY (nunca coloque a chave em arquivo do repositório).
  Windows (PowerShell):  $env:ELEVENLABS_API_KEY = "sua-chave"
  macOS/Linux:           export ELEVENLABS_API_KEY="sua-chave"

Uso: python gen_sfx.py   -> cria sfx/*.mp3 e sfxn/*.wav (pico em -3 dB) e confere que não estão mudos
"""
import json, os, re, subprocess, urllib.request

KEY = os.environ.get("ELEVENLABS_API_KEY")
if not KEY:
    raise SystemExit("Defina ELEVENLABS_API_KEY antes de rodar.")
PROMPTS = json.load(open(os.path.join(os.path.dirname(__file__), "sfx_prompts.json"), encoding="utf8"))
os.makedirs("sfx", exist_ok=True); os.makedirs("sfxn", exist_ok=True)

def gen(name, text, dur):
    out = f"sfx/{name}.mp3"
    if os.path.exists(out):
        return out
    body = json.dumps({"text": text, "duration_seconds": max(0.5, dur), "prompt_influence": 0.55}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body,
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json"}, method="POST")
    open(out, "wb").write(urllib.request.urlopen(req, timeout=120).read())
    return out

def level(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True)
    mx = re.search(r"max_volume: (-?[\d.]+)", r.stderr); mean = re.search(r"mean_volume: (-?[\d.]+)", r.stderr)
    return float(mx.group(1)), float(mean.group(1))

for name, (text, dur) in PROMPTS.items():
    src = gen(name, text, dur)
    mx, _ = level(src)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", f"volume={-3 - mx}dB,aresample=48000", "-ac", "2",
                    f"sfxn/{name}.wav"], check=True)
    mx2, mean2 = level(f"sfxn/{name}.wav")
    flag = "  <-- MUDO? regenere com 'loud, clear, close-up'" if mx2 < -10 or mean2 < -45 else ""
    print(f"{name:10s} pico {mx2:6.1f} dB  média {mean2:6.1f} dB{flag}")
