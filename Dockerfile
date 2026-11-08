FROM nginx:alpine

# Cấu hình nginx tĩnh: gzip, cache, /healthz
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Site thuần tĩnh, không có bước build
COPY index.html styles.css app.js /usr/share/nginx/html/

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1/healthz > /dev/null || exit 1
