<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is the RabbitMQ management plugin

> [!abstract] Short answer
> The management plugin ships with the broker and exposes an HTTP API plus a browser UI on port 15672 (15671 for TLS), alongside the rabbitmqadmin CLI. It collects and aggregates cluster metrics, manages users, vhosts, policies, and topology, and its Prometheus counterpart is recommended for long-term monitoring.

## What it gives you

The UI shows queues with ready/unacked breakdowns, message rates, consumers, connections and channels, node memory and disk state, and quorum health; it also handles topology and permission administration — declaring exchanges and queues, setting policies, creating users. The HTTP API under it (documented, scriptable with curl) is how CI pipelines and internal tools operate the broker. rabbitmqadmin wraps common operations for shell scripts.

```d2
direction: down
mgmt: "management plugin" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
ui: "UI\n:15672 browser" {
  width: 170
  height: 80
  style.fill: "#fff3e0"
}
api: "HTTP API\nmanagement + automation" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
admin: "rabbitmqadmin\nCLI wrapper" {
  width: 190
  height: 80
  style.fill: "#fff3e0"
}
mgmt -> ui
mgmt -> api
mgmt -> admin
```

**Fig. 1.** One plugin, three surfaces: browser UI, HTTP API, and the admin CLI.

## Operational notes

The management port speaks HTTP only — pointing an AMQP client at 15672 is a classic misconfiguration. Default credentials are guest/guest restricted to localhost; remote access requires creating real users, which is part of [[How do you secure RabbitMQ]]. For long-term storage, alerting, and dashboards, the docs recommend Prometheus over scraping the management API; the metric breakdown is in [[What RabbitMQ metrics do you monitor]].

```bash
rabbitmq-plugins enable rabbitmq_management
rabbitmqadmin queues list --vhost prod
```

**Listing 1.** Enable the plugin, then use the bundled CLI to read queue state; the same data is one GET on the HTTP API.

> [!warning] UI metrics are aggregated, not transactional
> The plugin samples and aggregates periodically, so rates during bursts or incidents are approximate; using management-API numbers for correctness decisions (billing, exactly-once anything) is wrong — it is an operator's telescope, not an application event log.

> [!tip] Interview answer
> It is the built-in ops surface: HTTP API and UI on 15672 plus rabbitmqadmin, giving queue, rate, consumer, connection, node, and quorum views with topology and permission management. Great for triage and automation; for long-term monitoring the docs point to Prometheus, and 15672 is HTTP, never AMQP.
