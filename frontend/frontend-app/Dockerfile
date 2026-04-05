FROM node:20-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html



#FROM node:20-slim AS builder

#WORKDIR /app

#COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
#COPY services/frontend ./services/frontend
#COPY packages ./packages

#RUN npm install -g pnpm
#RUN pnpm install
#RUN pnpm --filter frontend build

#FROM nginx:alpine
#COPY --from=builder /app/services/frontend/build /usr/share/nginx/html
