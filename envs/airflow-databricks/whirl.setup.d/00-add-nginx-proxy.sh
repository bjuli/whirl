#!/usr/bin/env bash

sudo bash -c 'echo -e 127.0.0.1\\tlogin.microsoftonline.com >> /etc/hosts'
sudo bash -c 'echo -e 127.0.0.1\\tlogin.microsoft.com >> /etc/hosts'
sudo bash -c 'echo -e 127.0.0.1\\tairflowlocaldev.azuredatalakestore.net >> /etc/hosts'

sudo bash -c 'cat > /etc/nginx/conf.d/locations.d/databricks-https-proxy.conf' << EOF
  location ~* /api/ {
    proxy_pass http://mockserver:1081;
  }
EOF

sudo bash -c 'cat > /etc/nginx/conf.d/locations.d/microsoft-https-proxy.conf' << EOF
  location ~* /common/ {
    proxy_pass http://mockserver:1081;
  }
  location ~* /some-fake-tenant/oauth2/token {
    proxy_pass http://mockserver:1081;
  }
  location ~* /webhdfs/ {
    proxy_pass http://mockserver:1081;
  }
EOF

sudo nginx -t && sudo service nginx restart
