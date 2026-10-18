# Receitas de cena

Todas foram usadas em vídeos reais. Tempos = palavra que dispara a ação.

## Texto atrás da pessoa
1. Gere o recorte: `npx hyperframes remove-background tight.mp4 -o person.webm --quality best`.
2. Camadas: vídeo original → texto gigante → `person.webm` (mesmas transformações de câmera do vídeo).
3. Posicione o texto de modo que o **cabelo cubra só a borda de baixo** — se cobrir demais, a palavra fica ilegível;
   se não cobrir, o efeito some. Teste com snapshot.
4. Entrada: `opacity 0, scale 1.14, blur 14px → 1, 1, 0` em 0,34 s.
5. Parede clara → texto escuro com degradê; parede escura → texto branco com degradê.

## Tela dividida
`.cam` (o vídeo) anima para `scale .5, y +420, clip-path inset(0 round 72px)` em 0,55 s (`power3.inOut`),
com uma sombra separada atrás. O topo (y 150–850) fica livre para o objeto 3D, ícones ou título.
Volta para tela cheia com corte seco na próxima frase.

## Cena só de texto (placa)
Placa `#f5f5f7` com halo branco radial. Linha 1 pequena cinza; linha 2 grande Geist 600; linha 3 em Fraunces
itálica entrando de x −1080 em 0,24 s. O bloco faz punch-in 1,07 → 1 e depois cresce 1 → 1,035 até o fim.
Ótima para a frase-tese ("a maior barreira é a **edição de vídeo**").

## Número que se transforma
"R$ 29,90 → 2990 centavos": cada caractere em posição absoluta calculada (largura fixa por dígito, `tabular-nums`).
O símbolo e a vírgula saem (opacity + blur), os dígitos deslizam juntos (`expo.inOut`), a unidade entra embaixo.
Mesma ideia para "2990 → 29.900000" (o ponto cai, os zeros entram, uma chave desenhada marca as casas decimais).

## Onda de áudio (cortes de silêncio)
Barras HTML deterministas em segmentos `fala | pausa | fala | pausa | fala`. Para mostrar o corte: segmentos de
pausa `scaleX → 0` e as falas seguintes deslizam para a esquerda pelo tamanho das pausas (só transforms).

## Objetos 3D (Three.js)
- Renderize **só** no evento `hf-seek` (determinístico, nada de `requestAnimationFrame`).
- `RoomEnvironment` + PMREM dão reflexos suaves; `ACESFilmicToneMapping`.
- Conversão de pixel para mundo: câmera fov 30, z 16 → `U = 2·16·tan(15°)/1920`.
- Exemplos que funcionaram: moeda (cilindro metálico, textura de face com "R$" — gire a textura 90°), cubo de
  cerâmica com ícone, banco de dados (3 cilindros + anéis), seringa transparente, tripla hélice, travesseiro
  (caixa arredondada "estufada" + vinco desenhado na superfície), bola de basquete (esfera com textura
  equiretangular), nó toroidal perolado.
- Objeto branco sobre fundo branco some: dê um tom levemente azulado/acinzentado e uma silhueta reconhecível.

## Objeto na mão da pessoa
1. Extraia quadros do trecho a 5 fps com grade e anote o centro da palma em cada um.
2. Faça uma tabela tempo → (x, y) e interpole. Mantenha o zoom em 1,0 nesse trecho (ou aplique a mesma transformação).
3. Objeto entra caindo com `outBack`, quica uma vez e gira devagar; sai com escala → 0 no corte seguinte.

## Telão atrás da pessoa
Moldura escura arredondada com leve `rotateX(6deg)`; tela azul-escura com grade de pontos de LED
(`radial-gradient` repetido + `mix-blend-mode: multiply`); texto com brilho (`text-shadow` em camadas).
Liga com `scaleY 0.02 → 1` + flash branco. Fica na camada "atrás", com o recorte da pessoa na frente.

## Cards, chips e listas
Vidro fosco (`rgba(255,255,255,.84)` + `backdrop-filter: blur(30px)` + sombra grande e suave), raio 44 px.
Entram com `back.out(1.4–1.8)`. Itens riscados: pseudo-elemento com `scaleX` animado via variável CSS.

## Notificação, busca, balão de prompt
Notificação estilo iOS (ícone + título + linha), campo de busca com letras digitadas uma a uma (cada letra é um
`<span>` com `opacity` — GSAP não anima `textContent`), balão azul de mensagem com ícone de enviar.

## Demonstrar recursos ao vivo
- "zoom" → punch-in forte (1,45) e volta.
- "transição" → whip: o vídeo desliza com blur, flash branco, volta do outro lado.
- "legendas dinâmicas" → aquele bloco de legenda aparece maior com `back.out`.
- "cortes de silêncio" → a onda de áudio perde as pausas.

## Encerramento
Placa clara, frase-tese (Geist + Fraunces) e pílula com o @ cujo contorno é desenhado
(`stroke-dasharray` com `pathLength="1"` animando `attr: {"stroke-dashoffset": 0}`).
