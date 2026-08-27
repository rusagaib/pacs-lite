# PACS-Lite

## Features:

- pacs orthanc
- worklist
- custom viewer dicom using custom ohif/viewers
- nginx conf for sso & non-sso
- change logo.png

## Quickstart:

### 1. clone this repo:

```sh
// using https
git clone https://github.com/rusagaib/pacs-lite.git
// or using ssh
git clone git@github.com:rusagaib/pacs-lite.git 
```

### 2. clone ohif viewer:

```sh
cd /pacs-lite
git clone -b release/3.12 https://github.com/OHIF/Viewers.git
```

### 3. build ohif Viewers image:

```sh
docker compose build --no-cache ohif_viewer
docker builder prune
docker images prune
```

### 4. run docker compose:

```sh
docker compose up -d
```

### 5. check running container images:

```sh
docker ps
```

### 6. check running container

```sh
docker stats
```

### 7. stop docker compose:

```sh
docker compose down
```

## Additional Config (NGINX):

### - nginx conf non sso (outer-client-config):

```sh
########################################################
# ohif-orthanc non sso
server {
    listen 8008;
    server_name _;

    # OHIF
    location /ohif/ {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;

        proxy_pass http://<REAL_IP_ADDR>:8043/;
    }

    # Orthanc
    location /orthanc/ {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;

        proxy_pass http://<REAL_IP_ADDR>:8043/orthanc/;
    }

    # Public assets
    location /public-assets/ {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;

        proxy_pass http://<REAL_IP_ADDR>:8043/public-assets/;
    }
}
```

### - nginx conf with sso (outer-client-config):

```sh
  ########################################################
  # ohif-orthanc 
  server {
    listen 443 ssl;
    server_name <HOST_DOMAIN_NAME>.xyz;

    location /ohif/ {
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   Host $host;
        proxy_pass http://127.0.0.1:8043/;
        # # translate headers from the outposts back to the actual upstream
        # auth_request_set $authentik_username $upstream_http_x_authentik_username;
        # auth_request_set $authentik_groups $upstream_http_x_authentik_groups;
        # auth_request_set $authentik_email $upstream_http_x_authentik_email;
        # auth_request_set $authentik_name $upstream_http_x_authentik_name;
        # auth_request_set $authentik_uid $upstream_http_x_authentik_uid;
        #
        # proxy_set_header X-authentik-username $authentik_username;
        # proxy_set_header X-authentik-groups $authentik_groups;
        # proxy_set_header X-authentik-email $authentik_email;
        # proxy_set_header X-authentik-name $authentik_name;
        # proxy_set_header X-authentik-uid $authentik_uid;
        #
        # ## Added
        # auth_request_set $authentik_auth $upstream_http_authorization;
        # proxy_set_header Authorization $authentik_auth;

        add_header Content-Security-Policy "frame-ancestors https://*.<HOST_DOMAIN_NAME>.xyz" always;
    }

    location /orthanc/ {
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   Host $host;
        proxy_pass http://127.0.0.1:8043;

        # authentik-specific config
        auth_request     /outpost.goauthentik.io/auth/nginx;
        error_page       401 = @goauthentik_proxy_signin;
        auth_request_set $auth_cookie $upstream_http_set_cookie;
        add_header       Set-Cookie $auth_cookie;

        # translate headers from the outposts back to the actual upstream
        auth_request_set $authentik_username $upstream_http_x_authentik_username;
        auth_request_set $authentik_groups $upstream_http_x_authentik_groups;
        auth_request_set $authentik_email $upstream_http_x_authentik_email;
        auth_request_set $authentik_name $upstream_http_x_authentik_name;
        auth_request_set $authentik_uid $upstream_http_x_authentik_uid;

        proxy_set_header X-authentik-username $authentik_username;
        proxy_set_header X-authentik-groups $authentik_groups;
        proxy_set_header X-authentik-email $authentik_email;
        proxy_set_header X-authentik-name $authentik_name;
        proxy_set_header X-authentik-uid $authentik_uid;

        ## Added
        auth_request_set $authentik_auth $upstream_http_authorization;
        proxy_set_header Authorization $authentik_auth;


        add_header Content-Security-Policy "frame-ancestors https://*.<HOST_DOMAIN_NAME>.xyz" always;
    }

    location /public-assets/ {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;

        proxy_pass http://127.0.0.1:8043/;

        add_header Content-Security-Policy "frame-ancestors https://*.<HOST_DOMAIN_NAME>.xyz" always;
    }

    location /outpost.goauthentik.io {
        proxy_pass              http://<SSO_PROVIDER_DOMAIN>:9000/outpost.goauthentik.io;
        proxy_set_header        Host $host;
        proxy_set_header        X-Original-URL $scheme://$http_host$request_uri;
        add_header              Set-Cookie $auth_cookie;
        auth_request_set        $auth_cookie $upstream_http_set_cookie;
        proxy_pass_request_body off;
        proxy_set_header        Content-Length "";
    }

    # Special location for when the /auth endpoint returns a 401,
    # redirect to the /start URL which initiates SSO
    location @goauthentik_proxy_signin {
        internal;
        add_header Set-Cookie $auth_cookie;
        return 302 /outpost.goauthentik.io/start?rd=$request_uri;
        # For domain level, use the below error_page to redirect to your authentik server with the full redirect path
        # return 302 https://authentik.company/outpost.goauthentik.io/start?rd=$scheme://$http_host$request_uri;
    }
  }
```

## Roadmap:

1. build docker images & push on image registry (github, docker-hub or private git vcs)


