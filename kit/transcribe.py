"""Transcrição com tempo por palavra (faster-whisper) + detector de voz (VAD).

Uso:
  python transcribe.py video.mp4                 -> words.json + imprime frases
  python transcribe.py video.mp4 --out w2.json
  python transcribe.py video.mp4 --vad           -> também imprime os trechos com voz
  python transcribe.py video.mp4 --clip 33.0 35.6  -> retranscreve só um trecho (para tirar dúvida)
"""
import argparse, json, subprocess, tempfile, os
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
from faster_whisper.vad import get_speech_timestamps, VadOptions

p = argparse.ArgumentParser()
p.add_argument("media")
p.add_argument("--out", default="words.json")
p.add_argument("--lang", default="pt")
p.add_argument("--model", default="large-v3-turbo")
p.add_argument("--vad", action="store_true")
p.add_argument("--clip", nargs=2, type=float)
a = p.parse_args()

wav = os.path.join(tempfile.gettempdir(), "_transcribe16k.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.media, "-ac", "1", "-ar", "16000", wav], check=True)
audio = decode_audio(wav, 16000)
model = WhisperModel(a.model, device="cpu", compute_type="int8")

if a.clip:
    s, e = a.clip
    segs, _ = model.transcribe(audio[int(s * 16000):int(e * 16000)], language=a.lang, beam_size=8, word_timestamps=True)
    print([(w.word.strip(), round(w.start + s, 2), round(w.end + s, 2)) for x in segs for w in x.words])
    raise SystemExit

if a.vad:
    ts = get_speech_timestamps(audio, VadOptions(min_silence_duration_ms=200, speech_pad_ms=60))
    print("VAD:", " ".join(f"({x['start']/16000:.2f},{x['end']/16000:.2f})" for x in ts))

segs, _ = model.transcribe(audio, language=a.lang, word_timestamps=True, vad_filter=False, beam_size=5)
words = []
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}")
    for w in s.words:
        words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 2)})
json.dump(words, open(a.out, "w", encoding="utf8"), ensure_ascii=False, indent=0)
print(f"{len(words)} palavras -> {a.out}")
