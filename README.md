# public-services

Services that are available for public usage.

## microk8s

On some bare-metal systems, microk8s is used to deploy Kubernetes.
For all other services, Managed Kubernetes installations, provided
by a Gardener instance, are used.

### Installation

```sh
apt-get install -y snapcraft
snap install microk8s --classic --channel=1.23/stable
snap install kubectl --classic
microk8s enable dns dashboard storage ingress
```

The following command will output the kubeconfig file from microk8s:

```sh
microk8s config
```

### Reset

```sh
microk8s reset --destroy-storage
microk8s enable dns dashboard storage ingress
```

## sto1

sto1 is a bare-metal system with 14x 16 TByte SATA HDDs. It is used to store logs of the CI
and container images. The storage is configured in a ZFS pool.

### Generic services sto1

```sh
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.7.2/cert-manager.yaml
kubectl apply -f generic/cert-manager.yaml
```

### Elasticsearch & Kibana services

* <https://elasticsearch.services.osism.tech/>
* <https://kibana.services.osism.tech/>

```sh
kubectl create -f https://download.elastic.co/downloads/eck/1.8.0/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/1.8.0/operator.yaml
kubectl apply -f sto1/logs.yaml
```

Get the credentials of the automatically created default user named ``elastic``:

```sh
kubectl get secret logs-es-elastic-user -o go-template='{{.data.elastic | base64decode}}'
```

### Harbor service

* <https://harbor.services.osism.tech>

```sh
helm repo add harbor https://helm.goharbor.io
```

```sh
helm install --create-namespace --namespace harbor harbor harbor/harbor --values sto1/harbor/harbor.yaml --set harborAdminPassword=password
```

```sh
helm upgrade --namespace harbor harbor harbor/harbor --values sto1/harbor/harbor.yaml
```

### Gitea service

* <https://gitea.services.osism.tech>

```sh
helm repo add gitea-charts https://dl.gitea.io/charts/
```

```sh
helm install --create-namespace --namespace gitea gitea gitea-charts/gitea --values sto1/gitea/values.yaml --set gitea.admin.password=password
```

```sh
helm upgrade --namespace gitea gitea gitea-charts/gitea --values sto1/gitea/values.yaml
```

## sto2

sto2 is a bare-metal system with 2x 8 TByte SATA HDDs. It is used to store machine images. Different to sto1, this system is not configured with a ZFS because minio cannot handle snapshots of ZFS and refuses to start at all (within kubernetes).

### Generic services sto2

```sh
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.7.2/cert-manager.yaml
kubectl apply -f generic/cert-manager.yaml
```

### Minio service

* <https://minio.management.osism.tech>
* <https://minio.services.osism.tech>

```sh
brew install krew
kubectl krew install minio
```

To be able to run kubectl plugins, you need to add the following to your ~/.zshrc:

```sh
export PATH="${PATH}:${HOME}/.krew/bin"
```

```sh
kubectl minio init --namespace-to-watch default -o > generic/minio-operator.yaml
kubectl apply -f generic/minio-operator.yaml
```

```sh
kubectl minio tenant create -o --servers 1 --volumes 4 --capacity 400Gi --storage-class microk8s-hostpath --enable-host-sharing minio --namespace default > sto2/minio/minio.yaml
kubectl apply -f sto2/minio/minio-secrets.yaml
kubectl apply -f sto2/minio/minio.yaml
```

```sh
kubectl minio proxy -n minio-operator
```
