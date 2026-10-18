# Editar vídeos com IA (Claude Code)

Treinamento completo para o **Claude Code** editar seus Reels/TikToks do jeito "estúdio": cortes de silêncio,
legendas dinâmicas, zooms, transições, texto atrás de você, elementos 3D, cenas de texto minimalistas e efeitos
sonoros — tudo sincronizado com a sua fala. Sem Premiere, sem CapCut, sem nenhum programa de edição instalado.

> Você grava falando normalmente para a câmera. O Claude transcreve, corta os erros e as pausas, cria as animações
> e entrega o MP4 pronto para postar.

---

## Como usar em 3 passos

### 1. Baixe este repositório
```bash
git clone https://github.com/ruyteer/editar-videos-com-ia.git
cd editar-videos-com-ia
```
Ou clique em **Code → Download ZIP** e descompacte.

### 2. Abra o Claude Code dentro da pasta e mande o seu vídeo
```bash
claude
```
O Claude lê o [`CLAUDE.md`](CLAUDE.md) automaticamente — é ali que está todo o treinamento.
Depois é só mandar o caminho do vídeo e explicar o que você quer:

```
Edita este vídeo: C:\Users\voce\Downloads\meu-video.mp4
Estilo minimalista, fundo claro, legendas bonitas. Meu @ é @seuperfil.
```

Usando o Claude em outro lugar (web, outro projeto)? Copie o [`PROMPT.md`](PROMPT.md) e cole no começo da conversa.

### 3. Peça a edição e aprove
O Claude mostra o plano de cortes e prints das cenas antes de renderizar. Você ajusta o que quiser e recebe o MP4
final (1080×1920, áudio em −14 LUFS, pronto para Reels/TikTok/Shorts).

---

## O que ele sabe fazer

| Recurso | Como fica |
|---|---|
| Cortes | Remove silêncios, gaguejos, começos falsos, frases repetidas e retomadas ("não gostei, vou de novo") |
| Ritmo | Pausas ≤ 0,2 s, fala 6–8 % mais rápida (mesmo timbre), zoom/corte a cada 1–4 s |
| Legendas | Frase curta inteira com fade suave, palavra-chave em serifada itálica |
| Texto atrás de você | Recorta a pessoa e coloca palavras gigantes entre você e a parede |
| 3D | Objetos limpos estilo Apple (moeda, cubo, banco de dados, bola, travesseiro…) que ilustram o que você fala |
| Cenas de texto | Telas claras e minimalistas com a frase-chave |
| Tela dividida | Seu vídeo vira um card e a ilustração aparece em cima |
| Instruções faladas | Você diz no vídeo "coloca uma bola na minha mão" e ele coloca |
| Efeitos sonoros | Gerados por IA (ElevenLabs), um em cada animação, abaixo da voz |
| Áudio | Limpeza de ruído, voz baixa fica alta, loudness padrão das redes |

---

## Requisitos

Instalados no seu computador (o Claude Code instala os que faltarem se você der permissão):

- [Claude Code](https://claude.com/claude-code)
- **ffmpeg** (corte, áudio e exportação)
- **Node.js 18+** (renderização das animações com [HyperFrames](https://hyperframes.heygen.com))
- **Python 3.9+** com `faster-whisper` (transcrição palavra por palavra)
- Opcional: chave da **ElevenLabs** para efeitos sonoros (plano Starter serve) — veja [`kit/README.md`](kit/README.md)

Rodando o Claude Code local, dê permissão para ele instalar as ferramentas e executar comandos na pasta.
Na nuvem, ele monta o ambiente sozinho.

---

## Estrutura

```
CLAUDE.md                 ← o treinamento (regras que o Claude segue)
PROMPT.md                 ← versão para copiar e colar
docs/
  playbook.md             ← fluxo completo, parâmetros e regras de gosto
  receitas-de-cena.md     ← como cada efeito é construído
  formatos.md             ← vários ângulos, B-roll, antes × depois, instruções faladas
  problemas-e-solucoes.md ← erros que já aconteceram e como evitar
kit/
  README.md               ← instalação e uso dos scripts
  transcribe.py           ← transcrição com tempo por palavra (+ detector de voz)
  cut.py                  ← corta, acelera, recorta 9:16 e trata o áudio
  gen_sfx.py              ← gera efeitos sonoros na ElevenLabs
  mix.py / finish.sh      ← mixa os efeitos e normaliza o loudness
  template/               ← composição base (legendas, zooms, cenas, 3D)
```

## Licença
MIT — use, adapte e compartilhe.
