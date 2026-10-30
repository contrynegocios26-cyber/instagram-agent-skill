/* =====================================================================
   MP Marcenaria — configuração do app
   Tudo que a marcenaria personaliza fica aqui: identidade, contatos,
   faixas de referência de preço, etapas do processo e dados de exemplo.
   Edite este arquivo; não é preciso mexer em app.js.
   ===================================================================== */
window.MP_CONFIG = {
  empresa: {
    nome: "MP Marcenaria",
    slogan: "Móveis planejados e esquadrias de alto padrão",
    cidade: "Alto Paraná – PR",
    atende: "Todo o Brasil, com foco no Paraná",
    anos: 5,
    instagram: "mp.marcenariaa",
    instagramUrl: "https://instagram.com/mp.marcenariaa",
    // Número no formato internacional, só dígitos. AJUSTE antes de publicar.
    whatsapp: "5544999999999",
    whatsappExibicao: "(44) 99999-9999",
    email: "contato@mpmarcenaria.com.br",
    cnpj: "00.000.000/0001-00",
    // Chave Pix usada no botão "copiar chave" dos pagamentos. AJUSTE.
    pixChave: "contato@mpmarcenaria.com.br",
    pixNome: "MP Marcenaria",
    garantiaMeses: 60,
    assistenciaMeses: 12
  },

  // PIN da área do marceneiro (modo oficina). Troque antes de publicar.
  pinOficina: "2026",

  /* Faixas de referência para a estimativa do cliente.
     R$ por metro linear de parede mobiliada (alto padrão), por ambiente.
     A estimativa é SÓ orientativa: o valor final sai do projeto executivo.
     precosConfigurados = false mostra o aviso "faixas de referência" no app. */
  precosConfigurados: false,
  referencia: {
    cozinha:     { min: 3800, max: 6200, icone: "cozinha",  label: "Cozinha" },
    suite:       { min: 2900, max: 4800, icone: "closet",   label: "Suíte / Closet" },
    banheiro:    { min: 2600, max: 4200, icone: "banheiro", label: "Banheiro" },
    sala:        { min: 2400, max: 4100, icone: "sala",     label: "Sala / Painel TV" },
    gourmet:     { min: 3600, max: 5900, icone: "gourmet",  label: "Área gourmet" },
    lavanderia:  { min: 2200, max: 3600, icone: "lavanderia", label: "Lavanderia" },
    escritorio:  { min: 2300, max: 3900, icone: "escritorio", label: "Home office" },
    portas:      { min: 1900, max: 4200, icone: "porta",    label: "Kit porta pronta", unidade: "porta" }
  },
  // Multiplicadores por padrão de acabamento
  padroes: [
    { id: "essencial", nome: "Essencial", fator: 0.82, desc: "MDF liso, ferragem com amortecedor, puxador perfil." },
    { id: "premium",   nome: "Premium",   fator: 1.00, desc: "Madeirado + liso fosco, fecho toque, LED sob aéreos." },
    { id: "assinatura",nome: "Assinatura",fator: 1.28, desc: "Ripados, painéis integrados, ferragem premium, vidro e metal." }
  ],
  extras: [
    { id: "led",      nome: "Iluminação LED embutida", fator: 0.06 },
    { id: "vidro",    nome: "Portas de vidro / espelho", fator: 0.08 },
    { id: "ferragem", nome: "Ferragem premium (Blum/Hettich)", fator: 0.10 },
    { id: "ripado",   nome: "Painel ripado integrado", fator: 0.12 }
  ],

  /* Etapas do processo, na linguagem do cliente.
     A ordem é a ordem real do serviço. */
  etapas: [
    { id: "contato",   nome: "Primeiro contato",   desc: "Entendemos o que você quer, o prazo e a verba." },
    { id: "medicao",   nome: "Medição na obra",    desc: "Visita técnica: paredes, pontos de água, luz e eletros." },
    { id: "projeto",   nome: "Projeto 3D",         desc: "Você recebe o 3D interativo e a proposta em PDF." },
    { id: "aprovacao", nome: "Aprovação",          desc: "Ajustes, assinatura digital e entrada." },
    { id: "remedicao", nome: "Remedição técnica",  desc: "Com piso e forro prontos, conferimos cada medida." },
    { id: "producao",  nome: "Produção",           desc: "Corte, usinagem, fita de borda e montagem na oficina." },
    { id: "entrega",   nome: "Entrega",            desc: "Transporte protegido até a obra." },
    { id: "instalacao",nome: "Instalação",         desc: "Montagem, nivelamento e regulagem de portas e gavetas." },
    { id: "garantia",  nome: "Garantia ativa",     desc: "Vistoria de entrega e assistência pelo período de garantia." }
  ],

  /* Acabamentos do catálogo (cores aproximadas para a visualização). */
  acabamentos: [
    { id: "carvalho",  nome: "Carvalho Hanover", tipo: "madeirado", cor: "#A47148", veio: true },
    { id: "nogueira",  nome: "Nogueira Terracota", tipo: "madeirado", cor: "#7A4A2E", veio: true },
    { id: "freijo",    nome: "Freijó Puro", tipo: "madeirado", cor: "#C4976A", veio: true },
    { id: "louro",     nome: "Louro Freijó", tipo: "madeirado", cor: "#B8895C", veio: true },
    { id: "branco",    nome: "Branco Supremo", tipo: "liso", cor: "#F3F1EC", veio: false },
    { id: "off",       nome: "Off White", tipo: "liso", cor: "#E9E3D8", veio: false },
    { id: "grafite",   nome: "Grafite Fosco", tipo: "liso", cor: "#3A3A3A", veio: false },
    { id: "verde",     nome: "Verde Jade", tipo: "liso", cor: "#4E6B5C", veio: false },
    { id: "areia",     nome: "Areia", tipo: "liso", cor: "#CFC2AE", veio: false },
    { id: "preto",     nome: "Preto Ébano", tipo: "liso", cor: "#1E1D1B", veio: false }
  ],

  /* Galeria de inspirações: cada item é uma elevação frontal desenhada pelo app
     (módulos em mm, cores por acabamento). Troque por fotos reais quando tiver
     (campo "foto": caminho ou data URI). */
  inspiracoes: [
    { id: "i1", ambiente: "cozinha", titulo: "Cozinha em L com torre quente", tags: ["madeirado", "LED", "fecho toque"],
      largura: 3400, altura: 2700, modulos: [
        { x: 0, y: 150, w: 900, h: 720, cor: "carvalho", frentes: 3 },
        { x: 900, y: 150, w: 600, h: 720, cor: "carvalho", frentes: 1 },
        { x: 1500, y: 150, w: 800, h: 720, cor: "carvalho", frentes: 2 },
        { x: 0, y: 1550, w: 1500, h: 700, cor: "branco", frentes: 2 },
        { x: 1500, y: 1550, w: 800, h: 700, cor: "branco", frentes: 1 },
        { x: 2340, y: 150, w: 1060, h: 2250, cor: "grafite", frentes: 0, torre: true }
      ]},
    { id: "i2", ambiente: "suite", titulo: "Closet aberto com LED", tags: ["ripado", "vidro", "LED"],
      largura: 3000, altura: 2600, modulos: [
        { x: 0, y: 100, w: 1000, h: 2400, cor: "nogueira", frentes: 1 },
        { x: 1000, y: 100, w: 1000, h: 2400, cor: "nogueira", frentes: 0, aberto: true },
        { x: 2000, y: 100, w: 1000, h: 2400, cor: "nogueira", frentes: 1 }
      ]},
    { id: "i3", ambiente: "sala", titulo: "Painel TV com porta camuflada", tags: ["ripado", "porta integrada"],
      largura: 4200, altura: 2700, modulos: [
        { x: 0, y: 0, w: 4200, h: 2700, cor: "freijo", frentes: 0, painel: true },
        { x: 300, y: 300, w: 1800, h: 450, cor: "grafite", frentes: 2 },
        { x: 3300, y: 0, w: 900, h: 2100, cor: "freijo", frentes: 1, porta: true }
      ]},
    { id: "i4", ambiente: "banheiro", titulo: "Gabinete suspenso com nicho", tags: ["liso fosco", "nicho LED"],
      largura: 1800, altura: 2000, modulos: [
        { x: 0, y: 450, w: 1200, h: 450, cor: "verde", frentes: 2 },
        { x: 1200, y: 450, w: 600, h: 450, cor: "verde", frentes: 0, aberto: true },
        { x: 0, y: 1300, w: 1800, h: 600, cor: "carvalho", frentes: 2 }
      ]},
    { id: "i5", ambiente: "gourmet", titulo: "Área gourmet com adega", tags: ["madeirado", "adega", "vidro"],
      largura: 3200, altura: 2600, modulos: [
        { x: 0, y: 150, w: 800, h: 720, cor: "louro", frentes: 2 },
        { x: 800, y: 150, w: 1200, h: 720, cor: "louro", frentes: 3 },
        { x: 2000, y: 150, w: 1200, h: 2250, cor: "preto", frentes: 0, torre: true },
        { x: 0, y: 1550, w: 2000, h: 450, cor: "areia", frentes: 3 }
      ]},
    { id: "i6", ambiente: "escritorio", titulo: "Home office com estante", tags: ["tampo 750", "nichos"],
      largura: 2800, altura: 2500, modulos: [
        { x: 0, y: 0, w: 2800, h: 750, cor: "carvalho", frentes: 0, tampo: true },
        { x: 0, y: 1200, w: 2800, h: 1300, cor: "branco", frentes: 0, aberto: true, nichos: 4 }
      ]},
    { id: "i7", ambiente: "portas", titulo: "Kit porta pronta frisada", tags: ["porta 900 × 2100", "batente sob medida"],
      largura: 1400, altura: 2400, modulos: [
        { x: 250, y: 0, w: 900, h: 2100, cor: "nogueira", frentes: 1, porta: true }
      ]},
    { id: "i8", ambiente: "lavanderia", titulo: "Lavanderia com torre de máquinas", tags: ["liso", "torre"],
      largura: 2400, altura: 2500, modulos: [
        { x: 0, y: 0, w: 700, h: 2400, cor: "branco", frentes: 0, torre: true },
        { x: 700, y: 900, w: 1700, h: 600, cor: "off", frentes: 0, aberto: true },
        { x: 700, y: 1700, w: 1700, h: 700, cor: "off", frentes: 2 }
      ]}
  ],

  /* ---------- Dados de exemplo (modo demonstração) ----------
     Substituídos quando o app recebe dados reais do cliente logado. */
  demo: {
    cliente: { nome: "Ana Beatriz", primeiroNome: "Ana", telefone: "(44) 99888-0000", cidade: "Maringá – PR", codigo: "MP-2026-0412" },
    projeto: {
      id: "ORC-MP-2026-0927-02",
      titulo: "Apartamento Jardim Novo Horizonte",
      arquiteto: "Studio Lume Arquitetura",
      etapaAtual: "producao",
      progresso: 62,
      previsaoEntrega: "2026-11-18",
      ambientes: [
        { nome: "Cozinha", valor: 38900, aprovado: true, status: "Em produção", detalhe: "Caixaria pronta. Frentes em acabamento." },
        { nome: "Suíte master", valor: 27400, aprovado: false, status: "Aguardando sua aprovação", detalhe: "Revisão 1 do 3D publicada em 24 out." }
      ],
      historico: [
        { data: "2026-09-27", etapa: "contato",   texto: "Primeiro contato pelo Instagram." },
        { data: "2026-10-02", etapa: "medicao",   texto: "Medição realizada. Obra com piso e forro prontos." },
        { data: "2026-10-09", etapa: "projeto",   texto: "Projeto 3D e proposta enviados." },
        { data: "2026-10-14", etapa: "aprovacao", texto: "Cozinha aprovada. Entrada recebida." },
        { data: "2026-10-16", etapa: "remedicao", texto: "Remedição técnica da cozinha concluída." },
        { data: "2026-10-20", etapa: "producao",  texto: "Cozinha entrou em produção." },
        { data: "2026-10-24", etapa: "projeto",   texto: "Suíte: revisão 1 publicada com a mudança do maleiro." }
      ],
      atualizacoes: [
        { data: "2026-10-28", titulo: "Frentes da cozinha", texto: "Portas e gavetas com fita de borda aplicada. Agora vão para a furação do fecho toque.", cor: "carvalho" },
        { data: "2026-10-23", titulo: "Caixaria cortada", texto: "Chapas cortadas no plano otimizado. Aproveitamento de 91 %.", cor: "branco" },
        { data: "2026-10-20", titulo: "Material chegou", texto: "MDF Carvalho Hanover e Branco Supremo recebidos e conferidos.", cor: "grafite" }
      ],
      pagamentos: [
        { n: 1, desc: "Entrada (40 %)", valor: 26520, vence: "2026-10-14", pago: true },
        { n: 2, desc: "Início da produção (30 %)", valor: 19890, vence: "2026-11-04", pago: false },
        { n: 3, desc: "Na instalação (30 %)", valor: 19890, vence: "2026-11-25", pago: false }
      ],
      documentos: [
        { nome: "Proposta comercial (R1)", tipo: "PDF", data: "2026-10-24" },
        { nome: "Contrato assinado", tipo: "PDF", data: "2026-10-14" },
        { nome: "Pranchas técnicas – Cozinha", tipo: "PDF", data: "2026-10-16" },
        { nome: "Ficha de medição", tipo: "PDF", data: "2026-10-02" }
      ],
      equipe: [
        { nome: "Marcelo", papel: "Projetista e dono", inicial: "M" },
        { nome: "Paulo", papel: "Produção", inicial: "P" },
        { nome: "Equipe de instalação", papel: "Montagem", inicial: "I" }
      ]
    },
    /* Projeto volumétrico usado no 3D (mm). Mesma lógica do projeto.json da MP. */
    projeto3d: {
      ambientes: [
        { nome: "Cozinha", largura: 3415, altura: 2698, profundidade: 3000,
          materiais: { M1: "#A47148", M2: "#F3F1EC", M3: "#3A3A3A" },
          modulos: [
            { id: "C01", tipo: "balcao", x: 30, y: 150, w: 900, h: 720, d: 560, caixa: "M2", frente: "M1", frentes: [{ tipo: "gaveta", qtd: 3 }] },
            { id: "C02", tipo: "balcao", x: 930, y: 150, w: 800, h: 720, d: 560, caixa: "M2", frente: "M1", frentes: [{ tipo: "porta", qtd: 2 }], pia: true },
            { id: "C03", tipo: "balcao", x: 1730, y: 150, w: 600, h: 720, d: 560, caixa: "M2", frente: "M1", frentes: [{ tipo: "porta", qtd: 1 }] },
            { id: "A01", tipo: "aereo",  x: 30, y: 1570, w: 1500, h: 700, d: 340, caixa: "M2", frente: "M2", frentes: [{ tipo: "porta", qtd: 2 }] },
            { id: "A02", tipo: "aereo",  x: 1530, y: 1570, w: 800, h: 700, d: 340, caixa: "M2", frente: "M2", frentes: [{ tipo: "porta", qtd: 1 }] },
            { id: "T01", tipo: "torre",  x: 2360, y: 150, w: 1025, h: 2250, d: 600, caixa: "M3", frente: "M3", frentes: [{ tipo: "porta", qtd: 2 }], nichos: [{ y: 900, h: 600 }, { y: 1500, h: 450 }] }
          ]},
        { nome: "Suíte master", largura: 3000, altura: 2600, profundidade: 3200,
          materiais: { M1: "#7A4A2E", M2: "#E9E3D8" },
          modulos: [
            { id: "R01", tipo: "roupeiro", x: 30, y: 100, w: 980, h: 2400, d: 600, caixa: "M2", frente: "M1", frentes: [{ tipo: "porta", qtd: 2 }] },
            { id: "R02", tipo: "roupeiro", x: 1010, y: 100, w: 980, h: 2400, d: 600, caixa: "M2", frente: "M1", frentes: [{ tipo: "porta", qtd: 2 }] },
            { id: "R03", tipo: "roupeiro", x: 1990, y: 100, w: 980, h: 2400, d: 600, caixa: "M2", frente: "M1", frentes: [{ tipo: "porta", qtd: 2 }] }
          ]}
      ]
    },
    notificacoes: [
      { id: "n1", data: "2026-10-28", titulo: "Nova foto da oficina", texto: "As frentes da sua cozinha ficaram prontas.", lida: false },
      { id: "n2", data: "2026-10-24", titulo: "Revisão do projeto da suíte", texto: "A revisão 1 está pronta para a sua aprovação.", lida: false },
      { id: "n3", data: "2026-10-20", titulo: "Produção iniciada", texto: "Sua cozinha entrou na linha de produção.", lida: true }
    ]
  },

  /* Cuidados e garantia, em linguagem de cliente. */
  cuidados: [
    { t: "Limpeza do dia a dia", d: "Pano macio levemente úmido e sabão neutro. Seque em seguida. Nada de álcool, abrasivo, esponja de aço ou produto com cloro." },
    { t: "Umidade", d: "MDF não gosta de água parada. Seque respingos na pia e no banheiro na hora e mantenha o ambiente ventilado." },
    { t: "Portas e gavetas", d: "Fechamento suave perde o ponto com o uso. A regulagem é simples: a MP faz na vistoria de garantia ou orienta por vídeo." },
    { t: "Peso nas prateleiras", d: "Prateleiras de 18 mm aguentam o uso normal. Para livros pesados ou louça, distribua o peso e use as prateleiras reforçadas." },
    { t: "Calor e sol", d: "Afaste forno, airfryer e cafeteira do tampo quando em uso. Sol direto todos os dias desbota o acabamento com o tempo." },
    { t: "Cupim e insetos", d: "MDF é tratado, mas a casa em obra pode trazer madeira bruta infestada. Qualquer pó fino nas quinas, fale com a MP." }
  ]
};
