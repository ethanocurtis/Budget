# ---- build stage ----
FROM node:20-slim AS build
WORKDIR /app

# Build context is ./frontend
COPY package.json pnpm-lock.yaml* ./
RUN corepack enable && corepack prepare pnpm@9.7.1 --activate
# lockfile may not match; allow resolver to update as needed
RUN pnpm install --no-frozen-lockfile

COPY . .
RUN pnpm build

# ---- serve stage (nginx) ----
FROM nginx:alpine AS serve
# Listen on 8080 so docker-compose mapping stays the same
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
