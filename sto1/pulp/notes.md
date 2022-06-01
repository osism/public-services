# Pulp how to

## preparation

```sh
sudo apt update
sudo apt -y install tmux tree htop screen docker.io
sudo usermod -a -G docker ubuntu
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -SL https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
sudo reboot

## confiugure repo

```sh
git clone https://github.com/pulp/pulp-operator.git
cd pulp-operator/containers
ln -s podman-compose.yml docker-compose.yml
```

Change the port of the pulp-web from 8080 to 80.

```sh
sed -i 's/      \- \"8080\:8080\"/      \- \"80\:8080\"/g' docker-compose.yml
```

File *compose/settings.py*

```py
SECRET_KEY = "aabbcc"
#CONTENT_ORIGIN = "http://localhost:24816"
CONTENT_ORIGIN = "http://<public_ip_without_port>"
DATABASES = {"default": {"HOST": "postgres", "ENGINE": "django.db.backends.postgresql", "NAME": "pulp", "USER": "pulp", "PASSWORD": "password", "PORT": "5432", "CONN_MAX_AGE": 0, "OPTIONS": {"sslmode": "prefer"}}}
REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_PASSWORD = ""
#ANSIBLE_API_HOSTNAME = "http://localhost:24817"
ANSIBLE_API_HOSTNAME = "http://pulp_api:24817"
TOKEN_SERVER = "localhost:24817/token/"
#TOKEN_AUTH_DISABLED = False
TOKEN_AUTH_DISABLED = True
TOKEN_SIGNATURE_ALGORITHM = "ES256"
PUBLIC_KEY_PATH = "/etc/pulp/keys/container_auth_public_key.pem"
PRIVATE_KEY_PATH = "/etc/pulp/keys/container_auth_private_key.pem"
```

File *compose/nginx/nginx.conf*

```ini
    (...)

    upstream pulp-content {
        #server localhost:24816;
        server pulp-content:24816;
    }

    upstream pulp-api {
        #server localhost:24817;
        server pulp-api:24817;
    }

    (...)
```

## How to add a remote etc

For .deb packages (bug opened <https://github.com/pulp/pulp_deb/issues/531>)

```sh
export name=test01
pulp deb repository create --name "${name}"
pulp deb remote create --name "${name}" --url http://nginx.org/packages/debian --distribution buster
pulp deb repository sync --name "${name}" --mirror --remote "${name}"
pulp deb distribution create --name "${name}" --base-path "${name}" --repository "${name}"
pulp deb publication create --repository "${name}" --simple True
#pulp deb publication create --repository "${name}" --structured True # is required for some reason before changing it to simple to get things working
```

For .rpm packages

```sh
export name=test02
pulp rpm repository create --name "${name}"
#pulp rpm remote create --name "${name}" --url https://download.ceph.com/rpm-pacific/el8/x86_64/
pulp rpm remote create --name "${name}" --url https://nginx.org/packages/rhel/9/x86_64/
pulp rpm repository sync --name "${name}" --mirror --remote "${name}" # full mirror
#pulp rpm repository sync --name "${name}" --no-mirror --remote "${name}" # only cache
pulp rpm distribution create --name "${name}" --base-path "${name}" --repository "${name}"
pulp rpm publication create --repository "${name}"
```

## Starting / Stopping

```sh
docker compose up -d
docker logs -f containers-pulp_api-1
# wait till all migrations are done you might find workers dying,
# especially when working on tasks with broken repo urls.
# Most commonly this can be identified by the worker-logs stating
# an error with the tmp directory.
# You just have to restart the workers than (maybe even multiple
# times). Not a nice, but working solution
docker compose down -v
```
