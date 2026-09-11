<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is message TTL and queue max-length in RabbitMQ

> [!abstract] Short answer
> Message TTL bounds how long a message may sit in a queue (`x-message-ttl` per queue or `expiration` per message, in milliseconds); max-length bounds how many (or how many bytes) a queue holds (`x-max-length`, `x-max-length-bytes`). Both expire or drop messages and both should point at a DLX so removal is observable, not silent.

## TTL mechanics

Per-queue TTL applies to every message entering; per-message TTL rides the `expiration` property as a string; when both exist the lower wins. Expiry is guaranteed not to be delivered, and removal happens when the message reaches the queue head (classic queues also expire on policy change; quorum queues expire at head). A TTL of 0 delivers immediately or expires on arrival. Queue TTL (`x-expires`) is a different feature: it deletes the whole unused queue after the idle period.

## Max-length and overflow

Max-length counts only ready messages — unacked ones do not count. When the limit is reached, the `x-overflow` setting decides: `drop-head` (default) discards oldest, `reject-publish` refuses new publishes and nacks them back through publisher confirms, `reject-publish-dlx` additionally dead-letters the rejected ones. Quorum queues support drop-head and reject-publish (imprecise overshoot documented), not reject-publish-dlx.

```d2
direction: down
in: "publish" {
  width: 140
  height: 60
  style.fill: "#e3f2fd"
}
q: "queue\nx-message-ttl, x-max-length" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
drop: "drop-head / reject-publish" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}
dlx: "DLX (if configured)" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
in -> q
q -> drop: "expired or over limit"
drop -> dlx
```

**Fig. 1.** TTL and length limits are removal rules; whether removal is visible depends on the DLX wiring.

```bash
rabbitmqctl set_policy bounds "^jobs$"   '{"max-length":100000,"message-ttl":3600000}' --apply-to queues
```

**Listing 1.** Both limits via one policy; policies are preferred over hardcoded x-arguments because they can change live.

> [!warning] Removal without a DLX is silent
> An expired or drop-head-discarded message that has no dead-letter configuration just disappears — consumers never learn a message was there. Logging, auditing, and retry systems all rely on pairing these limits with a DLX; the pattern is [[What is a RabbitMQ dead letter exchange]].

> [!tip] Interview answer
> TTL caps residence time — per-queue x-message-ttl or per-message expiration, lower wins, expiry at head — and max-length caps ready-message count or bytes, with drop-head, reject-publish, or reject-publish-dlx overflow. Both are policy-friendly x-arguments, and both should feed a DLX so removal is observable, the mechanism of [[What is a RabbitMQ dead letter exchange]]; the delay application is [[How do you delay a message in RabbitMQ]].
