#!/usr/bin/env bash
# Gera a pasta dist/ (PWA completa) a partir de src/.
# A mesma fonte (src/page.html) também é publicada como Artifact no claude.ai.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf dist && mkdir -p dist
{
  cat <<'HEAD'
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="App do cliente da MP Marcenaria: orçamento, acompanhamento da obra, aprovação do projeto 3D, pagamentos e pós-venda.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>
HEAD
  # <title>, metas e <link> de estilo vão para o head; o resto para o body
  sed -n '1,/^<link rel="stylesheet" href="styles.css">$/p' src/page.html | grep -v 'claude:viewport-fit-sides'
  echo '</head>'
  echo '<body>'
  sed '1,/^<link rel="stylesheet" href="styles.css">$/d' src/page.html
  echo '</body>'
  echo '</html>'
} > dist/index.html
cp src/styles.css src/app.js src/config.js src/sw.js src/manifest.webmanifest src/icon.svg dist/
[ -f src/icon-192.png ] && cp src/icon-192.png src/icon-512.png dist/ || true
echo "dist/ pronto: $(ls dist | tr '\n' ' ')"
