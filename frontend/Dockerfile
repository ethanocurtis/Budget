FROM node:20-slim AS build
WORKDIR /app

# Build context is ./frontend — copy files directly
COPY package.json pnpm-lock.yaml* ./
RUN corepack enable && corepack prepare pnpm@9.7.1 --activate

# Lockfile in repo may not match; allow pnpm to resolve fresh
RUN pnpm install --no-frozen-lockfile

COPY . .
RUN pnpm build

FROM node:20-slim AS serve
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@9.7.1 --activate
COPY --from=build /app/dist ./dist
EXPOSE 8080
CMD ["pnpm", "exec", "vite", "preview", "--host", "0.0.0.0", "--port", "8080"]
