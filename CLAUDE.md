# Regras deste repositório

## Conteúdo da MP Marcenaria

Todo conteúdo de Instagram da MP Marcenaria (@mp.marcenariaa) fica em
`conteudo/`. As regras completas estão em `conteudo/LEIA-ME.md`. Sempre que
você fizer, receber ou publicar um conteúdo:

- Uma pasta por post, `AAAA-MM-DD_tipo_tema` (tipo: reel, carrossel, foto,
  story), dentro da pasta do status: `1-postados`, `2-prontos-para-postar`,
  `3-em-producao` ou `4-ideias`. Fotos e vídeos ainda sem destino vão para
  `0-material-bruto`.
- Os arquivos do post e um `info.md` vão dentro da pasta. Use
  `python conteudo/catalogo.py novo ...` para criar e
  `python conteudo/catalogo.py postar ...` quando for ao ar.
- Se os arquivos ficam no PC do usuário, preencha `arquivos_pc` com o caminho
  relativo a `conteudo_redes_sociais`.
- Rode `python conteudo/catalogo.py` no fim e faça commit de `CATALOGO.md` e
  `catalogo.csv` junto.
- Nada é postado sem o usuário dizer sim.
