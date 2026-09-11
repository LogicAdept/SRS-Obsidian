<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is the Kafka Quota API for?

> [!abstract] Short answer
> Broker-enforced throttling of clients so one loud producer or consumer cannot monopolize broker resources in a shared cluster: byte-rate limits on produce and fetch traffic (since 0.9) and a CPU-share limit on request threads (since 0.11), attached to user and client-id groups and enforced by delaying responses — not by disconnecting anyone. Managed with `kafka-configs.sh` or programmatically through the Admin client ([[What core Kafka APIs exist]]).

## What is limited, and for whom

Kafka defines two client quota families. *Network bandwidth quotas* cap the byte rate of produce and fetch requests. *Request rate quotas* cap the percentage of time a client group may occupy the request handler and network threads — a quota of `n%` means `n%` of one thread, out of a total capacity of `(num.io.threads + num.network.threads) * 100%` per broker, which makes it effectively a CPU limit. Quotas attach to three identity shapes: the `(user, client-id)` pair, the user principal alone, or the client-id alone; for each connection the most specific matching quota applies, with a fixed precedence order from exact pair down to defaults. All members of a quota group *share* the limit: 10 MB/s for `(user1, clientA)` is split across every producer instance that user runs with that id. By default clients are unlimited, and limits live as overrides in the metadata log — every broker reads them, so changes take effect immediately without a rolling restart.

```bash
bin/kafka-configs.sh --bootstrap-server localhost:9092 --alter \
  --add-config 'producer_byte_rate=1024,consumer_byte_rate=2048,request_percentage=200' \
  --entity-type users --entity-name user1 --entity-type clients --entity-name clientA

bin/kafka-configs.sh --bootstrap-server localhost:9092 --describe \
  --entity-type users --entity-name user1 --entity-type clients --entity-name clientA
```

**Listing 1.** Setting and inspecting a quota for one (user, client-id) pair; replacing `--entity-name` with `--entity-default` sets the group's default limit.

The same operations exist in code: `Admin.describeClientQuotas` and `Admin.alterClientQuotas` ([[What is the Kafka AdminClient API for]]). Custom limit lookups — per-tenant plans, for example — plug in through the broker's `client.quota.callback.class` setting ([[How do you secure a Kafka cluster]]). Quota windows also exist for internal traffic, separate from client quotas: replication, alter-log-dirs moves, and controller mutations each carry their own throttles so cluster repair work cannot starve client traffic.

## How enforcement feels to a throttled client

```d2
direction: down
req: "Client request\n(produce or fetch)" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
check: "Broker: over quota in\nthe measurement window?" {
  width: 320
  height: 100
  style.fill: "#fff3e0"
}
delay: "Response with delay,\nfetch responses empty;\nchannel muted" {
  width: 320
  height: 110
  style.fill: "#ffebee"
}
wait: "Client refrains from\nsending during the delay" {
  width: 320
  height: 100
  style.fill: "#f3e5f5"
}
resume: "Traffic resumes under quota" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
req -> check
check -> delay: violation
check -> resume: within quota
delay -> wait -> resume
```

**Fig. 1.** Violation is answered, not killed: the broker computes the delay needed to bring the client back under quota, returns a response carrying that delay, and mutes the channel until it elapses.

Usage is measured over multiple small windows — on the order of thirty one-second samples — so violations are caught and corrected quickly; one large window would produce traffic bursts followed by long stalls. The throttle works from both sides: a well-behaved client that receives a non-zero delay refrains from sending further requests, and even old clients that ignore the delay are held back because the broker mutes their socket channel. A throttled fetch returns a response with no data, so the observable symptom on the client is growing lag, not an error ([[What is Kafka consumer lag and how do you debug it]]).

> [!warning] Quotas are per broker, not cluster-wide
> A 1 MB/s bandwidth quota means 1 MB/s *against each broker* — a client talking to ten brokers can move ten times that in aggregate. This is a deliberate design choice (sharing usage across brokers would need its own coordination), but it surprises anyone doing capacity math, and it is why throttled consumers show lag on only some partitions ([[What Kafka broker settings matter in practice]]).

> [!tip] Interview answer
> Quotas protect multi-tenant clusters: byte-rate limits on produce and fetch plus a CPU-share limit on request threads, attached to user, client-id, or their pair, with the most specific match winning. Brokers enforce them per broker by responding with a computed delay and muting the channel — clients slow down rather than break. You set them with kafka-configs.sh or the Admin quota methods, and they apply immediately without restarts.

