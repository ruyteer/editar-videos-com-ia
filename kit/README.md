# Kit de scripts

## Instalação (uma vez)

```bash
# Python (transcrição)
pip install faster-whisper

# ffmpeg: https://ffmpeg.org/download.html  (Windows: winget install Gyan.FFmpeg)

# Template de composição (Node 18+)
cd kit/template
npm install
node setup.mjs                      # copia fontes e bibliotecas para public/
npx hyperframes browser ensure      # baixa o Chrome usado no render
```

Efeitos sonoros (opcional): crie uma chave na ElevenLabs e defina a variável de ambiente — **nunca** salve a chave
em arquivo do repositório.

```bash
export ELEVENLABS_API_KEY="sua-chave"          # macOS/Linux
$env:ELEVENLABS_API_KEY = "sua-chave"          # Windows PowerShell
```

## Uso, na ordem

```bash
# 1. transcrever o bruto (+ trechos com voz)
python kit/transcribe.py bruto.mp4 --vad

# 2. escrever keep.json com os trechos a manter, ex.: [[0.8,4.5],[6.3,9.6]]
#    e cortar (acelera 1.07x, entrega 1080x1920)
python kit/cut.py bruto.mp4 keep.json tight.mp4 --speed 1.07
#    vídeo fora de 9:16?  --crop 423:752:30:0     voz baixa?  --boost 10

# 3. retranscrever o corte (tempos definitivos)
python kit/transcribe.py tight.mp4 --out words2.json

# 4. (opcional) recorte da pessoa para texto/objetos atrás dela  (~15 min)
cd kit/template && npx hyperframes remove-background ../../tight.mp4 -o public/person.webm --quality best

# 5. compor: edite kit/template/src/index.html (procure "EDITE AQUI"), copie tight.mp4 para public/ e monte
cp ../../tight.mp4 public/
node build.mjs ../../words2.json 42.5 "@seuperfil"
npx hyperframes lint public
npx hyperframes snapshot public --at 1,5,10 --no-end -o snaps     # OLHE os prints

# 6. renderizar
npx hyperframes render public -q high -f 30 -w 4 -o master.mp4

# 7. efeitos + loudness (cues.json = [[tempo, "nome", ganho], ...])
python ../gen_sfx.py
bash ../finish.sh master.mp4 cues.json 2.8 final.mp4
```

## QC antes de postar

```bash
# folha geral a 2 quadros/s
ffmpeg -i final.mp4 -vf "fps=2,scale=120:-1,tile=16x8" -frames:v 1 qc.jpg
# só a faixa da legenda (procure legenda presa/sobreposta)
ffmpeg -i final.mp4 -vf "fps=2,crop=1080:300:0:1400,scale=160:-1,tile=12x12" -frames:v 1 qc_legenda.jpg
```

Alvo: −14 LUFS, pico ≤ −1,5 dBTP, nenhum quadro vazio, uma legenda por vez, efeitos audíveis.
