<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Java/Security #SRS

# How do you secure a Kafka cluster

> [!abstract] Short answer
> **Three pillars, all per-listener config: authentication (SSL client certs or SASL — SCRAM, Kerberos/GSSAPI, PLAIN, OAUTHBEARER), encryption (TLS for client-broker and broker-broker traffic), and authorization (pluggable authorizer with ACLs — "principal P is allowed/denied operation O on resource R").** A production cluster also isolates listeners, rotates credentials, and treats an unauthenticated plaintext listener as an incident.

## The Kafka security model

Kafka's official security overview lists the supported measures: authentication of clients, other brokers and tools via SSL or SASL (with the SASL mechanisms GSSAPI/Kerberos since 0.9, PLAIN since 0.10.0, SCRAM-SHA-256/512 since 0.10.2, OAUTHBEARER since 2.0); encryption of data in transit with SSL — with an acknowledged CPU performance cost; and authorization of read/write operations, pluggable so external authorization services can integrate.

```d2
direction: right
prod: "Producer" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
tls: "TLS: encrypt in transit\nSASL/SCRAM or mTLS: authenticate" {
  width: 360
  height: 100
  style.fill: "#fff3e0"
}
broker: "Broker\nauthorizer + ACLs" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
acl: "ACL: principal P allowed\ndescribe on topic T" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}
cons: "Consumer" {
  width: 190
  height: 70
  style.fill: "#e3f2fd"
}
prod -> tls -> broker
broker -> tls -> cons
broker -> acl
```

**Fig. 1.** Every hop is authenticated and encrypted; the broker's authorizer decides each read/write against ACLs.

The authorization side has a concrete syntax in the docs: ACLs follow "Principal {P} is [Allowed|Denied] Operation {O} From Host {H} on any Resource {R} matching ResourcePattern {RP}", managed with `kafka-acls.sh`; the authorizer is plugged in with `authorizer.class.name` (for KRaft clusters: `org.apache.kafka.metadata.authorizer.StandardAuthorizer`). Notably, a resource with no ACLs is closed — only super users get in.

```java
# server.properties (KRaft) — the three pillars wired together
listeners=SASL_SSL://:9092
listener.security.protocol.map=SASL_SSL:SASL_SSL
sasl.enabled.mechanisms=SCRAM-SHA-512
authorizer.class.name=org.apache.kafka.metadata.authorizer.StandardAuthorizer
ssl.keystore.location=/etc/kafka/ssl/broker.keystore.p12
ssl.truststore.location=/etc/kafka/ssl/broker.truststore.p12

# grant least-privilege access
kafka-acls.sh --bootstrap-server broker:9092 --add \
  --allow-principal User:orders-service \
  --operation Read --operation Describe \
  --topic orders
```

**Listing 1.** Conceptual configuration (from the documented properties): a single SASL_SSL listener, SCRAM-SHA-512 authentication, the KRaft standard authorizer, and an ACL that lets one service principal read one topic.

> [!warning] Encryption is not authentication, and default open ACLs are gone
> The traps. First, "we enabled TLS" only fixes eavesdropping — without SASL or client certs anyone can still connect and (on an unauthorized-by-default cluster... or worse, one left with open ACLs) produce or consume; the docs support mixed authenticated/unauthenticated and encrypted/non-encrypted listeners, which is exactly how insecure listeners survive into production. Second, SCRAM credentials live in the metadata log — but the SASL/PLAIN mechanism transmits cleartext passwords and is only safe behind TLS, and OAUTHBEARER needs a callback handler wired for token validation; mechanism choice is a real decision. Third, ACLs are per-operation and per-host-pattern: a service principal with "Allow all on *" defeats the model — grant Read/Describe/Write narrowly per topic and consumer group ([[How do Kafka consumers fetch messages from a broker]] shows the consumer side that ACLs protect). Fourth, broker-to-broker links need the same treatment (inter-broker protocol), or an attacker on the network segment impersonates a broker. Where this meets Spring: [[How do you configure a Spring Kafka producer and listener]] carries the client-side credentials.

> [!tip] Interview answer
> **Kafka security is three pillars per listener: authenticate with SASL — SCRAM-SHA-512 or OAUTHBEARER in modern clusters, Kerberos or PLAIN in older ones — or mTLS; encrypt with TLS for client-broker and broker-broker traffic; authorize with a pluggable authorizer and ACLs like "orders-service may read topic orders". ACL resources without rules are closed to everyone but super users. Rotate credentials, keep one secured listener, and never leave an open plaintext port next to a secured one.**

