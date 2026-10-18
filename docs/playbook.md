# Playbook de edição

## 1. Gosto — o que funciona e o que não funciona

### Funciona
| Item | Detalhe | Por quê |
|---|---|---|
| Estética Apple minimalista | `#f5f5f7` ou preto, Geist + Fraunces itálica com degradê na palavra de ênfase, 1 cor de destaque | Limpo, premium, legível no celular |
| 3D que ilustra a fala | Objetos de cerâmica/alumínio/vidro, luz suave (Three.js) | "Mostra" o conceito sem tirar a atenção da pessoa |
| Alternância de cenas | Pessoa → só texto → tela dividida → 3D | Retenção — o olho sempre tem algo novo |
| Texto atrás da pessoa | Palavra gigante entre a pessoa e a parede, com o cabelo na frente | Efeito "premium" muito usado em Reels de alto alcance |
| Tela dividida | Vídeo encolhe para um card com cantos arredondados; ilustração em cima | Dá espaço sem tirar a pessoa da tela |
| Cards numerados | "causa 01", "passo 2", "✓ solução" em vidro fosco | Estrutura listas e tutoriais |
| Demonstração ao vivo | Quando a pessoa cita "zoom", entra um zoom; "transição", entra uma transição | O vídeo prova o que diz |
| Efeitos sonoros | Um por animação, audíveis, abaixo da voz | Dá "peso" a cada elemento |

### Não funciona
| Item | Por quê |
|---|---|
| Legenda animando palavra por palavra no tempo exato | Parece que o texto "travou" / "lagou" |
| Legenda com contorno grosso estilo TikTok antigo | Visual datado |
| Efeito sonoro inaudível | Se não dá para ouvir, não existe |
| Arte abstrata, metal líquido, aurora, dourado como protagonista | Rouba a cena da pessoa/produto |
| Pausas longas e ritmo lento | O público sai |
| Música no arquivo | Problema de direitos — coloque pelo app |

## 2. Fluxo (pedido → entrega)

1. **Receber** o vídeo e copiar para uma pasta de projeto.
2. **Diagnóstico**: `ffprobe`; folha de quadros; `volumedetect`; grade sobre um quadro para medir cabeça, rosto,
   queixo e espaço livre.
3. **Transcrição** com tempo por palavra.
4. **Erros**: cruzar transcrição + VAD + retranscrição isolada de trechos suspeitos.
5. **Roteiro de corte** (`keep.json`), explicando ao usuário o que sai.
6. **Corte limpo** com `kit/cut.py`.
7. **Retranscrever o corte** (tempos definitivos + confere que nada foi cortado).
8. **Plano de cenas** sobre os tempos novos.
9. **Recorte da pessoa** em segundo plano, só se for usar.
10. **Composição** → lint → snapshots → corrigir.
11. **Render** → mix dos SFX → loudnorm → QC.
12. **Entrega** com resumo.

## 3. Parâmetros

### Transcrição
- faster-whisper `large-v3-turbo`, CPU, `int8`, `word_timestamps=True`, `beam_size=5`, `language="pt"`.
- VAD (`get_speech_timestamps`, `min_silence_duration_ms=180–200`, `speech_pad_ms=60`) quando houver ruído.
- Trecho duvidoso: retranscreva só ele (beam 8, volume +8 dB).

### Corte e ritmo
- Margem 0,06–0,08 s nas bordas; micro-fade de 12–15 ms no áudio de cada trecho.
- Aceleração 1,06–1,08× (`setpts` + `atempo`).
- Punch-in a cada troca de frase: `scale S×1,07 → S` em 0,32 s (`power2.out`), alternando 1,0 (aberto) e
  1,12–1,25 (close), com a origem no rosto. Para mostrar as mãos: escala 1,3 + deslocamento em y.

### Vídeo
- `scale=1080:1920:flags=lanczos,unsharp=5:5:0.5,eq` leve, `fps=30`.
- `libx264 -crf 16 -preset slow -g 30 -keyint_min 30 -pix_fmt yuv420p` — keyframes densos evitam quadro
  congelado no render.
- ffmpeg 7+/9: use `-/filter_complex arquivo.txt` (o antigo `-filter_complex_script` saiu) e `-fps_mode vfr`.

### Áudio da voz
- `highpass=80–90`, `afftdn` moderado, `volume` se a voz estiver baixa, `acompressor` (−20/−22 dB, 3:1),
  `alimiter`. Redução de ruído forte demais deixa a voz robótica.
- Final: loudnorm 2 passadas `I=-14:TP=-2:LRA=11`, `linear=true`, AAC 192k, `+faststart`.

### Legendas
- Até 3 palavras; quebra em pontuação ou pausa > 0,35 s; **junte blocos com < 0,5 s**.
- Entrada: fade + subida 14 px em até 0,2 s (≤ 40 % da duração do bloco), ~0,04 s antes da 1ª palavra.
- Saída: fade 0,1 s, que só começa **depois** que a entrada termina. Use `fromTo` com `immediateRender:false`
  nos dois — um `to` cruzando um `fromTo` deixa o bloco preso na tela.
- Branca Geist 600 ~66 px com sombra; palavra-chave Fraunces itálica ~80 px com degradê.
- Posição: faixa escura e estável (peito/camiseta/cabelo), dentro da área segura (y ≈ 1380–1560).
- Esconda durante cenas de texto, telas divididas e cards grandes.

### Efeitos sonoros
- ElevenLabs `POST /v1/sound-generation`, prompts curtos terminando em "short, dry, no music";
  `prompt_influence 0.55`. Som fraco? acrescente "loud, clear, close-up".
- Normalize pelo pico (−3 dB) e **confira** que o arquivo tem som.
- Mix: `adelay` + `amix normalize=0`; ganho por efeito 0,12–0,30 × 2,8 (~7 dB abaixo dos picos da voz).

| Momento | Efeito |
|---|---|
| Troca de cena / tela dividida | whoosh |
| Card ou texto deslizando | swish |
| Item aparecendo | pop / tick |
| Título forte | thud |
| Solução / ✓ | chime |
| Riscado / errado | error / strike |
| Zoom | zoom whoosh |
| Transição | whip |
| Encerramento | shimmer + click |

### Render
- HyperFrames `render -q high -f 30 -w 4` (~3–5 min para 40–70 s).
- Recorte da pessoa: `remove-background --quality best` (~12–18 min na CPU para 40–70 s).

## 4. Áreas seguras (9:16)
Evite texto importante no topo (~150 px), no rodapé (~350–430 px) e na coluna direita (~120 px).
Conteúdo-chave entre y ≈ 150 e 1500.
