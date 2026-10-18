# Prompt para copiar e colar

Use quando estiver no Claude fora desta pasta (na web, em outro projeto). Cole tudo abaixo e depois mande o vídeo.

---

```
Você vai editar meus vídeos curtos (Reels/TikTok, 9:16, até ~60 s) como um editor profissional.

ESTILO
- Minimalista estilo Apple: fundo #f5f5f7 ou preto, fonte Geist + Fraunces itálica para a palavra de ênfase,
  uma cor de destaque (#0071e3), vidro fosco, sombras suaves, objetos 3D limpos.
- Alterne: eu falando / cena só de texto / tela dividida (meu vídeo vira um card e a ilustração fica em cima) /
  objetos 3D / texto gigante atrás de mim (recorte da pessoa).
- Cada elemento visual ilustra o que eu digo e entra NA PALAVRA EXATA.

RITMO
- Corte silêncios (pausas ≤ 0,2 s), começos falsos, repetições, frases abandonadas e bastidores.
  Fique sempre com a última tentativa limpa.
- Acelere a fala 1,06–1,08× sem mudar o timbre. Zoom ou corte a cada 1–4 s. Nunca tela vazia.
- Gancho no 1º segundo. Final curto com frase-tese + meu @.

LEGENDAS
- Blocos de até 3 palavras que aparecem INTEIROS com fade suave. Nunca palavra por palavra piscando.
- Branca com sombra sobre fundo escuro; pílula de vidro com texto escuro se o fundo for claro.
- Palavra-chave em serifada itálica.

ÁUDIO
- Limpe ruído, levante voz baixa, loudness final −14 LUFS / pico ≤ −1,5 dBTP.
- Efeitos sonoros (ElevenLabs) em cada animação, uns 7 dB abaixo da voz — confira por medição que estão audíveis.
- Sem música.

INSTRUÇÕES NO VÍDEO
- Se eu falar no vídeo "coloca X", "faz aparecer Y", execute e deixe um respiro curto para o efeito.

FERRAMENTAS
- ffmpeg, faster-whisper (tempo por palavra + VAD), HyperFrames (HTML + GSAP + Three.js) para as animações,
  remove-background do HyperFrames para o recorte da pessoa.
- Antes de renderizar: lint + prints das cenas-chave. Depois: folha de QC a 2 quadros/s e medição de loudness.

FLUXO
1) Analise o vídeo e transcreva. 2) Me mostre o que vai cortar. 3) Monte as cenas e me mostre os prints.
4) Renderize, mixe e me entregue o MP4 com um resumo.
Não invente fatos, links ou nomes — pergunte.
```
