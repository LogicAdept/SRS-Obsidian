<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is the difference between clustering federation and shovel in RabbitMQ

> [!abstract] Short answer
> Clustering makes many nodes one logical broker over a trusted LAN. Federation links independent brokers by replicating exchange flows or serving queue demand across AMQP links. Shovel is a lower-level unidirectional mover: a configured consumer that republishes from a source queue to a destination exchange. They combine — clusters linked by federation or shovels.

## The three models

A cluster shares metadata, requires compatible versions and the Erlang cookie, and assumes LAN-like networks: one broker, any node serves any client. Federation keeps brokers fully independent, connected by AMQP (optionally TLS): federated *exchanges* copy an upstream's message flow into downstream exchanges — bindings propagate upstream so unmatched messages are not forwarded; federated *queues* pull from upstreams only when local consumers want messages, preferring local ones. Shovel is an explicit queue-to-exchange transfer worker with acknowledges on both ends; dynamic shovels are policy-configured, static ones defined in config, and RabbitMQ 4.2 added local shovels over an internal API.

```d2
direction: down
cl: "clustering\none broker, LAN, CP-leaning" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
fe: "federation\nindependent brokers, selective copy" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
sh: "shovel\nexplicit unidirectional move" {
  width: 270
  height: 90
  style.fill: "#ffebee"
}
```

**Fig. 1.** From one logical broker to independent brokers copying flows to a point-to-point message mover — and the edges compose, per [[What is RabbitMQ clustering]] and [[What happens when a RabbitMQ node crashes]].

## Choosing

Cluster for availability and capacity inside one data centre. Federate for geo pub/sub, gradual migrations, and cross-version or cross-cluster linking where independence matters. Shovel for controlled migrations, one-off bridges, aggregating remote sources, or cross-protocol moves (it supports AMQP 0-9-1 and 1.0 endpoints). CAP-flavoured summary from the distributed docs: federation/shovel lean AP over WAN links, clustering leans CP inside the LAN.

```bash
rabbitmqctl set_parameter federation-upstream up1   '{"uri":"amqps://upstream.example.com"}'
rabbitmqctl set_parameter shovel move-orders   '{"src-uri":"amqp://a", "src-queue":"orders",
    "dest-uri":"amqp://b", "dest-exchange":"orders"}'
```

**Listing 1.** Both are runtime parameters: a federation upstream and a dynamic shovel definition.

> [!warning] Federation is not replication
> A federated exchange forwards messages it can route downstream, and a federated queue moves data toward consumers — neither copies everything unconditionally like a mirror. Expecting federation to behave as full-copy replication produces topologies where "missing" messages were simply unroutable downstream.

> [!tip] Interview answer
> Clustering: one logical broker, shared metadata, LAN, versions and cookie must match. Federation: independent brokers linked over AMQP, exchange federation copies routable flows, queue federation serves demand toward consumers. Shovel: a unidirectional mover you configure queue-to-exchange, great for migrations. All three combine.
