# Problemas que já aconteceram (e como evitar)

| Problema | Causa | Solução |
|---|---|---|
| Efeitos sonoros entregues mudos | Um `afade=t=out:st=0:d=0.001` na normalização zerou os arquivos | Normalize só com `volume`; meça cada WAV e meça o mix num trecho sem voz |
| Legenda "presa" na tela, sobrepondo as próximas | Bloco curto: o fade de entrada (0,2 s) terminava depois do fade de saída começar | Junte blocos < 0,5 s; entrada ≤ 40 % do bloco; saída só depois da entrada; `fromTo` + `immediateRender:false` |
| Legenda "piscando" palavra por palavra | Animação por palavra no tempo exato | Bloco inteiro com fade |
| Ruído de fundo quase no volume da voz | Ventilador / ar-condicionado | `silencedetect` não funciona → use VAD; `afftdn` moderado; recomende gravar sem ventilador ou com lapela |
| Duas tentativas coladas numa frase só | Whisper | Retranscreva o trecho isolado |
| Nome próprio errado ("Cloud" em vez de "Claude") | Whisper | Corrija só no texto exibido; confirme a grafia com a pessoa |
| Frase sumiu no corte | Bug no script de trechos | Sempre retranscreva o corte e compare com o roteiro |
| Texto atrás da pessoa não aparece "atrás" | Texto acima da cabeça, sem sobreposição | Desça até o cabelo cobrir a borda de baixo; sem espaço acima da cabeça, não use |
| Texto atrás coberto demais | Desceu demais | Uma linha só, mais alta |
| Textura 3D girada 90° | Mapeamento UV da tampa do cilindro | `texture.center.set(.5,.5); texture.rotation = π/2` |
| Objeto 3D branco "some" no fundo branco | Pouco contraste | Tom levemente azulado + silhueta reconhecível |
| Quadro vazio depois de um corte | Elemento entrava segundos depois | O elemento principal entra no próprio corte |
| Palavra grande quebrando linha e encostando em outro elemento | Largura | `white-space: nowrap`, fonte menor, mais espaço |
| Lint `gsap_non_transform_motion` | Animando `top/left/width/height` | Anime `x/y/scale/opacity` |
| GSAP não anima texto | `textContent` não é interpolável | Um elemento por estado/letra, alternando `opacity` |
| Render com Chrome travado em `requestAnimationFrame` | Aba oculta não roda rAF | Lógica determinística por tempo (`hf-seek`) / `setTimeout` em scripts de captura |
| Arquivos sumiram entre sessões | Pasta temporária limpa automaticamente | Trabalhe numa pasta de projeto permanente |
| Comando travado esperando entrada | `cat > arquivo` sem heredoc | Sempre use heredoc ou a ferramenta de escrita de arquivo |
