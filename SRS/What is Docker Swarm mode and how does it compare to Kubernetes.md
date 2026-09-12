<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #DevOps/Tools/Kubernetes #SRS

# What is Docker Swarm mode and how does it compare to Kubernetes

> [!abstract] Short answer
> Swarm mode is the orchestrator built into the Docker Engine: `docker swarm init` turns hosts into managers and workers, and a **service** declares the desired replica count that managers continuously reconcile into tasks (containers). It ships in the CLI with zero extra install, uses Raft consensus between managers, gives every service a DNS name with a load-balancing VIP, and publishes ports through a routing mesh — dramatically simpler than Kubernetes, with a far smaller ecosystem.

## The machinery

Managers keep cluster state in a Raft log (an odd count, typically 3 or 5, tolerates `(N-1)/2` failures) and schedule tasks onto workers over mutual-TLS connections. A service is declarative: `docker service create --replicas 3` stores the desired state, and the reconciliation loop starts or replaces tasks wherever they diverge. Discovery uses the embedded DNS: a service name resolves to a virtual IP whose traffic spreads over the healthy tasks ([[How do containers find each other by name on a Docker network]]). Tasks talk over an **overlay** network that spans nodes ([[What are the Docker network drivers and when should you use each]]), and any published port is answered by the routing mesh on **every** node, which forwards to a healthy task anywhere in the cluster.

```bash
docker swarm init                      # this node becomes the first manager
docker service create --name api \
  --replicas 3 --publish 8080:8080 \
  api:1.42
docker service ls                      # desired vs replicated count
docker service ps api                  # task placement and state
```

**Listing 1.** The whole cluster bring-up is three engine commands — no control-plane install, no CNI choice, no etcd to babysit.

## The comparison in one view

Kubernetes models much more: pods as scheduling units, controllers, jobs, stateful sets, autoscaling, CRDs, and a controller-manager/scheduler/etcd control plane that needs real installation and operations expertise ([[What is Kubernetes]]). Swarm's model — services of replicas — is easier to learn and operate, but the price is a thinner feature set: no equivalent of pod-level controllers, a much smaller ecosystem of tooling, and community momentum concentrated on Kubernetes ([[How does Docker differ from Kubernetes]] frames the same contrast from the container side). Compose's `deploy:` section only reaches full effect on a Swarm, which is how single-host stacks graduate to a cluster without changing tooling.

> [!warning] "Swarm is deprecated" is a lie — but so is "it is the safe default"
> Swarm mode still ships inside the Engine and is not officially deprecated. What actually happened: Docker's enterprise business moved to Mirantis in 2019, ecosystem investment flowed to Kubernetes, and most job-market and tooling gravity is there. Answering "Swarm, because K8s is complex" without mentioning ecosystem cost — or "K8s, because Swarm is dead" — are both wrong; the honest framing is simplicity versus ecosystem.

> [!tip] Interview answer
> Swarm mode is Docker's built-in orchestrator: managers hold cluster state in Raft, services declare a replica count, and the reconciler keeps tasks matching it. It gives service DNS with a load-balancing VIP, an overlay network between nodes, and a routing mesh that answers published ports on any node. Compared to Kubernetes it is far simpler to run but has a smaller feature set and ecosystem; I would pick it for small clusters that want self-healing without operating a full control plane, and Kubernetes when autoscaling, ecosystem, or hiring patterns matter more.
