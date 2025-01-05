import express from "express";
import { services } from "./config/services.js";
import { createServiceProxy } from "./utils/proxyFactory.js";

class Gateway {
  #app;
  #services;

  constructor() {
    this.#app = express();
    this.#services = services;
    this.#setupMiddleware();
    this.#setupRoutes();
    this.#setupErrorHandler();
  }

  #setupMiddleware = () => {
    this.#app.use((req, res, next) => {
      console.log(
        `${new Date().toISOString()} - ${req.method} ${req.originalUrl}`
      );
      next();
    });
  };

  #setupRoutes = () => {
    Object.values(this.#services).forEach((service) => {
      this.#app.use(service.pathPrefix, createServiceProxy(service));
    });

    this.#app.get("/health", (_, res) => {
      res.json({ status: "healthy" });
    });
  };

  #setupErrorHandler = () => {
    this.#app.use((err, req, res, _) => {
      console.error(err.stack);
      res.status(500).send("Something broke in the gateway!");
    });
  };

  start = (port = process.env.PORT ?? 3000) => {
    this.#app.listen(port, () => {
      console.log(`API Gateway running on port ${port}`);
      console.log("Registered services:");
      Object.entries(this.#services).forEach(([name, service]) => {
        console.log(`- ${name}: ${service.pathPrefix} → ${service.url}`);
      });
    });
  };
}

const gateway = new Gateway();
gateway.start();

export default Gateway;
