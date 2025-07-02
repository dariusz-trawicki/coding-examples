# Example: Kafka with Strimzi - on Minikube 

This example based on an example from the official documentation.
https://strimzi.io/quickstarts/

## Run `Minikube`

```bash
minikube start --memory=8192 --cpus=4 --driver=docker
```

## Deploy Strimzi using installation files

Before deploying the Strimzi cluster operator, create a namespace called kafka:

```bash
kubectl create namespace kafka
```

```bash
# Deploy Strimzi using installation files
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
# You can find the code in tmp/01-strimzi-install-latest-kafka.yaml.

# Optional:
# Follow the deployment of the Strimzi cluster operator:
# kubectl get pod -n kafka --watch
# follow the operator’s log:
# kubectl logs deployment/strimzi-cluster-operator -n kafka -f
```

## Create an Apache Kafka cluster

```bash
# Create a new Kafka custom resource to get a single node Apache Kafka cluster:
# Apply the `Kafka` Cluster CR file
kubectl apply -f https://strimzi.io/examples/latest/kafka/kafka-single-node.yaml -n kafka
# You can find the code in tmp/kafka-single-node.yaml

# Wait while Kubernetes starts the required pods, services, and so on:
kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka 
# The above command might timeout if you’re downloading images over a slow connection. If that happens you can always run it again.
# *** Output *** 
# kafka.kafka.strimzi.io/my-cluster condition met
```

## Send and receive messages

### To Send the messages, run:

```bash
kubectl -n kafka run kafka-producer -ti --image=quay.io/strimzi/kafka:0.46.0-kafka-4.0.0 --rm=true --restart=Never -- bin/kafka-console-producer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic
# *** Output *** 
# If you don't see a command prompt, try pressing enter.
# >
#
# ### Type your message after the “>” symbol and press Enter, e.g.:
# >Hello 1
# >Hello 2
# >etc.
# NOTE: Each line represents one Kafka message sent to the my-topic topic. 
```

### To receive the messages, run (in a different terminal):

```bash
kubectl -n kafka run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.46.0-kafka-4.0.0 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic --from-beginning
# *** Output *** 
# ...
# Hello 1
# Hello 1
# etc.
```

## Cleaning

```bash
# Deleting your Apache Kafka cluster
kubectl -n kafka delete $(kubectl get strimzi -o name -n kafka)
kubectl delete pvc -l strimzi.io/name=my-cluster-kafka -n kafka

# Deleting the Strimzi cluster operator
kubectl -n kafka delete -f 'https://strimzi.io/install/latest?namespace=kafka'


## Deleting the kafka namespace
kubectl delete namespace kafka
```