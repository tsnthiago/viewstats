# Estágio 1: Builder - Constrói a aplicação
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install -g npm@latest
RUN npm install
COPY . .
RUN npm run build

# Estágio 2: Runner - Serve a aplicação construída
FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app .
EXPOSE 3000
CMD ["npm", "start"] 