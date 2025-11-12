FROM node:20-alpine
WORKDIR /app
COPY server.js .
RUN npm init -y && npm install ws
ENV PORT=8080
EXPOSE 8080
CMD ["node", "server.js"]
