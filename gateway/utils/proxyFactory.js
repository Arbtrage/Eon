import { createProxyMiddleware } from "http-proxy-middleware";

export const createServiceProxy = (service) => {
  return createProxyMiddleware({
    target: service.url,
    changeOrigin: true,
    pathRewrite: {
      [`^${service.pathPrefix}`]: "",
    },
    onError: (err, req, res) => {
      console.error(`Proxy error: ${err}`);
      res.status(500).send(`Service ${service.pathPrefix} unavailable`);
    },
  });
};
