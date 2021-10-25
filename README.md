# public-serivces

## microk8s

On some bare-metal systems, microk8s is used to deploy Kubernetes.
For all other services, Managed Kubernetes installations, provided
by a Gardener instance, are used.

### Installation

```
snap install microk8s --classic --channel=1.23/stable
microk8s enable dns dashboard storage ingress
```

### Reset

```
microk8s reset --destroy-storage
microk8s enable dns dashboard storage ingress
```

## sto1

sto1 is a bar-metal system with 14x 16 TByte SATA HDDs. It is used to store logs of the CI
and binary artifacts like container images or machine images.

### Generic services

### Elasticsearch & Kibana services

```
kubectl create -f https://download.elastic.co/downloads/eck/1.8.0/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/1.8.0/operator.yaml
kubectl apply -f sto1/elasticsearch.yml
kubectl apply -f sto1/kibana.yml
```
