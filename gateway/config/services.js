export const services = {
  chat: {
    url: process.env.CHAT_SERVICE_URL ?? "http://localhost:3001",
    pathPrefix: "/chat",
  },
  embedding: {
    url: process.env.EMBEDDING_SERVICE_URL ?? "http://localhost:3002",
    pathPrefix: "/embedding",
  },
  api: {
    url: process.env.API_SERVICE_URL ?? "http://localhost:3003",
    pathPrefix: "/api",
  },
};
