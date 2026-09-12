<!--
reps: 0
priority: 0
-->
#Security/NetworkSecurity #SRS

# What is a DMZ in network security

> [!abstract] Short answer
> A DMZ (demilitarized zone) is an intermediate network segment - classically "a network created by connecting two firewalls" (NIST SP 800-41) - where systems that must be reachable from the internet live while the internal LAN stays behind the second firewall. The traffic policy is asymmetric: internet reaches only DMZ hosts on published ports, DMZ hosts cannot freely reach the LAN, and LAN-initiated flows are answered deliberately.

## The two-firewall layout

```d2
direction: right
net: "Internet" { width: 150; height: 60; style.fill: "#ffebee"
fw1: "Edge firewall" { width: 180; height: 70; style.fill: "#e3f2fd"
dmz: "DMZ\nreverse proxy, mail, web" { width: 280; height: 90; style.fill: "#fff3e0"
fw2: "Inner firewall" { width: 180; height: 70; style.fill: "#e3f2fd"
lan: "LAN\napps, DB, users" { width: 200; height: 80; style.fill: "#e8f5e9"
net -> fw1 -> dmz -> fw2 -> lan
```

**Fig. 1.** The canonical three-homed design. A single-firewall variant puts the DMZ on a separate interface with the same rule semantics; the invariant is that a DMZ compromise is not a LAN foothold.

The rule set that makes a DMZ mean something:

- **Internet -> DMZ**: only the published services (443 to the reverse proxy, 25 to mail); everything else dropped.
- **DMZ -> LAN**: denied by default; when a flow is needed (proxy to app on one port), it is an explicit narrow rule - and the app tier holds its own allow-list toward the DB tier.
- **LAN -> DMZ**: allowed for administration, ideally from a management segment.
- **State and logging**: flows are stateful and logged; the DMZ is where the WAF and TLS termination typically sit ([[What is a WAF]]).

## Why the DB does not live in the DMZ

Public hosts are assumed compromisable - they run parse-heavy services against untrusted input. The DMZ accepts that: those hosts contain no data worth protecting beyond their own state, hold no credentials that open the LAN wide (a reverse proxy holds routes, not DB passwords), and are monitored as hostile territory ([[What is defense in depth]] is the logic; [[What is network segmentation]] generalizes the practice).

> [!warning] "We have a DMZ, so the app in it can talk to the database directly with a root account"
> Then the DMZ is only a drawing. The value is in the **edges**: a DMZ host with a wildcard route to the LAN and a DBA credential in its config is a LAN host with better optics. Narrow rules, scoped credentials, and egress filtering are what make the zone real ([[What is the principle of least privilege]] at network scale).

> [!tip] Interview answer
> A DMZ is the buffer segment between two firewalls where internet-facing hosts live: internet reaches DMZ services on published ports, DMZ-to-LAN is deny-by-default with explicit narrow exceptions, and nothing in the DMZ holds LAN-opening credentials. It is the classic perimeter answer - and in zero-trust designs the same isolation shows up as micro-segments instead of one big zone.
