# Construa a partir da raiz do repositório:
#   docker build -f app/Dockerfile -t marina-app .
ARG BASE=node:22-alpine
FROM ${BASE}
ENV NODE_ENV=production
WORKDIR /app
COPY app/package.json app/package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force
COPY app/server.js ./
COPY app/lib ./lib
COPY app/public ./public
COPY app/dados-exemplo ./dados-exemplo
COPY app/scripts ./scripts
COPY skills/marina-atendimento/SKILL.md ./skill/SKILL.md
RUN mkdir /dados && chown node:node /dados
ENV DADOS_DIR=/dados PORT=3000
VOLUME /dados
USER node
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD wget -qO- http://localhost:3000/saude || exit 1
CMD ["node", "server.js"]
