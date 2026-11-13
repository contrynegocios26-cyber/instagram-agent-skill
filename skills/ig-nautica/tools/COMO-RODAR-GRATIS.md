# Como gerar as artes e os vídeos de graça (sem gastar tokens)

Os scripts desta pasta rodam no seu computador, sem internet e sem pagar nada.
Só o Claude consome tokens. Os programas abaixo são gratuitos e de código aberto.

## Instalar uma vez (Windows, Mac ou Linux)
1. Python 3.11 ou mais novo: python.org
2. FFmpeg: ffmpeg.org (no Windows: `winget install ffmpeg`)
3. No terminal:
   pip install pillow numpy "rembg[cpu]" piper-tts
   python -m piper.download_voices pt_BR-faber-medium
4. Fontes: Inter e Archivo (gratuitas no Google Fonts). Ajuste os caminhos em `country.py`.

## Para cada jet novo
1. Recorte: `rembg i foto.jpg recorte.png`
2. Copie um arquivo de `unidades/` (ex.: gtx230_25.json) e troque modelo, ano, horas, preço e as falas.
3. Rode:
   python gen_unit.py unidades/novo.json        (7 slides, quadrado, stories e 3 Reels)
   python santarosa.py unidades/novo.json reel  (jet na Prainha de Santa Rosa + Reel)

## Alternativa sem programação (também grátis)
- CapCut: legendas automáticas e vozes em português (texto para fala), com modelos de Reels.
- Canva grátis: monte um modelo com o layout da Country e só troque a foto e o preço.
O que eu monto aqui serve de modelo para copiar nesses apps.
