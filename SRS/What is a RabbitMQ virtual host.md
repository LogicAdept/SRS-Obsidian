<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is a RabbitMQ virtual host

> [!abstract] Short answer
> A vhost is a namespace inside one broker: its own exchanges, queues, bindings, policies, and its own user permissions. Connections always target exactly one vhost, and nothing inside a vhost can reference entities in another. The default vhost is named `/`.

## What isolation means here

RabbitMQ is multi-tenant: every topology entity belongs to a vhost, and permissions are granted per vhost, so a user with access to `prod` cannot see or touch anything in `qa`. Logical separation is the goal — physical resource partitioning is not; vhosts share the same node memory, disk, and CPU, though certain per-vhost limits (connections, queues) can be configured. Cross-vhost data flow happens only through applications that connect to both, or through the Shovel plugin. Compare this with [[What is RabbitMQ clustering]], where replication crosses nodes inside one logical broker rather than namespaces.

```d2
direction: right
conn1: "connection 1\nvhost /prod" {
  width: 210
  height: 90
  style.fill: "#e3f2fd"
}
conn2: "connection 2\nvhost /qa" {
  width: 200
  height: 90
  style.fill: "#e3f2fd"
}
prod: "vhost /prod\nexchanges, queues, perms" {
  width: 250
  height: 100
  style.fill: "#fff3e0"
}
qa: "vhost /qa\nexchanges, queues, perms" {
  width: 240
  height: 100
  style.fill: "#ffebee"
}
conn1 -> prod
conn2 -> qa
```

**Fig. 1.** Each connection is scoped to one vhost; the two namespaces share broker resources but not topology or permissions.

## Operations

Vhosts are created with `rabbitmqctl add_vhost` or the HTTP API; each fresh vhost gets the pre-declared exchanges only, and users must be granted `configure`, `write`, and `read` permissions before connecting. A per-vhost default queue type (for example, making quorum the default) can be set, which is how teams roll out quorum-first policies without rewriting declarations.

```bash
rabbitmqctl add_vhost staging
rabbitmqctl set_permissions -p staging appuser ".*" ".*" ".*"
```

**Listing 1.** Create a vhost and grant the app user configure, write, and read permissions on it.

Splitting environments this way is the first step of [[How do you secure RabbitMQ]], because permission scopes are enforced per vhost.

> [!warning] A vhost is not a security boundary against the node
> Vhosts isolate topology and permissions, but they share the broker process and its resource limits: a memory alarm, disk alarm, or node crash hits every vhost at once. Presenting vhosts as hard multi-tenancy for hostile tenants overstates the isolation.

> [!tip] Interview answer
> A vhost is RabbitMQ's tenant namespace — its own topology, policies, and permission scope, with the default `/` vhost out of the box. Connections target exactly one vhost, permissions are per-vhost, and isolation is logical, not physical: alarms and node failures are shared across all vhosts.
