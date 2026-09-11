<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# How do you secure RabbitMQ

> [!abstract] Short answer
> Layer the basics: TLS on client and management listeners (amqps 5671, HTTPS 15671), real users with least-privilege per-vhost permissions instead of guest, loopback-only default user, firewalled ports, disabled unused plugins, and OAuth 2/LDAP backends when the organisation has them.

## Identity and permissions

Authentication and authorisation are separate. Connections present username-password, a JWT (OAuth 2), or an x.509 certificate; authorisation then checks `configure`, `write`, and `read` permissions per vhost per resource, with topic-level authorisation available for topic exchanges. The default guest user only works from localhost by design — remote guest connections are refused — and production brokers replace it with named, least-privileged users bound to the vhosts they need.

```d2
direction: down
tls: "TLS listeners\n5671, 15671, plugin twins" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
authn: "authenticate\npassword / JWT / x.509" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
authz: "authorise\nconfigure/write/read per vhost" {
  width: 270
  height: 90
  style.fill: "#fff3e0"
}
net: "network\nfirewall, loopback guest" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
tls -> authn -> authz
net <- -> authn
```

**Fig. 1.** Security is layered: encrypted transport, verified identity, scoped permissions, network boundaries.

## Transport and network

Enable TLS listeners for client traffic and the management UI; certificates can also authenticate clients (external/certificate backend). The inter-node cluster links and CLI tool distribution are separate surfaces that also need network discipline — the cookie in [[What is RabbitMQ clustering]] is a credential as much as a config value. Lock the port surface: 5672/5671 for AMQP, 15672/15671 management, plugin ports only where needed, everything else firewalled — this is also the perimeter story for [[What is a RabbitMQ virtual host]] tenancy.

```bash
listeners.tcp = none
listeners.ssl.default = 5671
management.ssl.port = 15671
```

**Listing 1.** The TLS-only posture: plain AMQP listeners off, AMQPS and HTTPS on.

> [!warning] Vhost permissions are not encryption
> A user granted ".*" on a vhost can read every queue there — wildcard permissions are not least-privilege, and TLS does not authorise. Teams that stop at "we use TLS" miss that any over-permissioned client can then consume everything inside its vhost.

> [!tip] Interview answer
> TLS everywhere including management, named users with per-vhost configure/write/read scoping, guest kept on localhost or removed, topic authorisation where routing is sensitive, OAuth 2 or LDAP as backends for enterprise identity, firewall the port surface, and disable unused plugins so the attack area stays small.
