FROM node:20-slim AS build
WORKDIR /app
COPY frontend/package.json frontend/pnpm-lock.yaml* ./
RUN corepack enable && corepack prepare pnpm@9.7.1 --activate
RUN pnpm install --frozen-lockfile
COPY frontend ./
RUN pnpm build

FROM node:20-slim AS serve
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@9.7.1 --activate
COPY --from=build /app/dist ./dist
# Minimal static server via vite preview
EXPOSE 8080
CMD ["pnpm", "exec", "vite", "preview", "--host", "0.0.0.0", "--port", "8080"]
