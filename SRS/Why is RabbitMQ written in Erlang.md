<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# Why is RabbitMQ written in Erlang

> [!abstract] Short answer
> RabbitMQ is an Erlang/OTP application: it runs on the Erlang virtual machine (BEAM), and Erlang must be installed alongside it. OTP's process model, supervision, pre-emptive scheduling, and built-in distribution fit a broker whose job is thousands of long-lived concurrent connections and failure containment.

## What OTP contributes

Erlang's processes are cheap, isolated, GC-per-process entities — one per queue, per channel, per connection in RabbitMQ — so a busy queue is one schedulable process rather than a thread-pool fight. Pre-emptive scheduling keeps one slow consumer's parser from stalling another queue's delivery loop. OTP supervision trees restart failed components without taking down the node, and the same failure-recovery machinery extends to clusters: nodes authenticate to each other with an Erlang cookie and communicate over Erlang distribution, which is why matching Erlang/OTP versions across nodes is a documented clustering requirement.

```d2
direction: down
beam: "BEAM VM\nschedulers per core" {
  width: 230
  height: 80
  style.fill: "#e3f2fd"
}
procs: "Erlang processes\nqueues, connections, channels" {
  width: 290
  height: 90
  style.fill: "#fff3e0"
}
sup: "OTP supervision\nrestart failed parts" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}
dist: "distribution\ncluster + CLI (cookie)" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
beam -> procs
procs -> sup
procs -> dist
```

**Fig. 1.** Broker components map onto Erlang processes under OTP supervision, with distribution providing clustering.

## The operational flip side

The same runtime is the operational cost: operators tune VM schedulers, allocators, and process limits in `rabbitmq.conf`/`advanced.config`, and CLI tools require the shared cookie. RabbitMQ documents strict Erlang/OTP compatibility per release series (for the 4.x series, Erlang 26 and 27, with 28 partially supported), so Erlang is not just an implementation detail but a versioning constraint for upgrades. The same distribution layer is what [[What is RabbitMQ clustering]] runs on, which is why the cookie appears there too.

```erlang
%% advanced.config — VM-level knobs belong to the broker's runtime
[
 {rabbit, [{default_consumer_prefetch, {false, 250}}]}
].
```

**Listing 1.** Broker configuration files are Erlang terms — evidence that the server itself is an Erlang application.

For what the broker does independent of its runtime, start from [[What is RabbitMQ]] and [[What is a RabbitMQ virtual host]].

> [!warning] Do not attribute everything to Erlang
> Claiming "Erlang makes RabbitMQ crash-proof" is a lie: a node can still OOM, run out of disk, or lose a quorum. Erlang gives isolation and restartability; durability and data safety come from quorum queues, confirms, and acks layered above it.

> [!tip] Interview answer
> RabbitMQ is an Erlang/OTP application — queues, connections, and channels are Erlang processes on BEAM. Erlang brings cheap concurrency, pre-emptive scheduling, supervision, and native distribution used for clustering and CLI. The trade-off is the operational model: Erlang version pinning, cookie-based auth, and VM tuning.
