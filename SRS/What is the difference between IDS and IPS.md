<!--
reps: 0
priority: 0
-->
#Security/NetworkSecurity #SRS

# What is the difference between IDS and IPS

> [!abstract] Short answer
> An IDS **detects and alerts** - it sits out-of-band on a mirrored port, sees copies of traffic, and reports; an IPS **prevents** - it sits inline in the traffic path and can drop, reject, or block automatically. NIST SP 800-94 treats both as IDPS (intrusion detection and prevention systems) distinguished by placement and response capability; the corollary is that an IDS cannot stop what it sees, and an IPS that misfires stops legitimate traffic.

## Placement decides the verb

```d2
direction: right
i: "Internet" { width: 130; height: 60; style.fill: "#ffebee"
fw: "Firewall" { width: 150; height: 60; style.fill: "#e3f2fd"
ips: "IPS\ninline, blocks" { width: 200; height: 70; style.fill: "#fff3e0"
lan: "LAN" { width: 130; height: 60; style.fill: "#e8f5e9"
ids: "IDS\nmirrored traffic, alerts only" { width: 280; height: 70; style.fill: "#fff3e0"
i -> fw -> ips -> lan
fw -> ids: "SPAN / TAP copy"
```

**Fig. 1.** The IPS is in the line and must be correct and fast; the IDS watches a copy and can afford deeper analysis - but only raises its hand.

- **IDS (passive)**: analyzes mirrored traffic or log streams; produces alerts for the SIEM; zero latency impact on the real flow; cannot act on the packet it inspected ([[What is a SIEM]] is where its alerts land).
- **IPS (inline)**: same detection engines plus enforcement - drop packets, reset connections, block source addresses; every false positive is a user-visible outage, so tuning bar and risk are higher.
- **Detection methodologies** (SP 800-94's taxonomy, shared by both): **signature-based** (known patterns - precise, blind to novel attacks), **anomaly-based** (statistical deviation from a baseline - catches the new, floods during baselining and infrastructure changes), and **stateful protocol analysis** (protocol-model violations - deep but resource-heavy).
- **Flavors**: network-based (NIDPS) at segment boundaries, host-based (HIDPS) per machine, wireless, and network behavior analysis.

## Choosing between them

Inline prevention wins where the traffic is well-understood and the cost of a false block is low (perimeter edge filtering known exploit patterns, legacy protocols); passive detection wins where traffic is business-critical and detection needs context (internal east-west monitoring, encrypted segments with selective decryption). Many organizations run both - inline IPS at the edge, passive sensors on core links - which is one reason the standards term is IDPS.

> [!warning] "An IPS is just an IDS that blocks, so deploy the IPS everywhere"
> The same detection engine behaves differently inline: what was an ignored alert becomes a dropped customer session, so signature gaps and anomalies turn into self-inflicted outages. Inline placement demands a tuning lifecycle - baseline, alert-only first, then selective prevention - and even then anomaly-mode blocking is rarely worth the risk ([[What is defense in depth]] wants layers, not one over-aggressive one).

> [!tip] Interview answer
> Same detection family, different placement: IDS is passive on a traffic copy - alerts only; IPS is inline and can drop or block in real time. Both run signature, anomaly, and stateful protocol analysis per NIST SP 800-94. I put prevention at well-understood edges and detection on core links, and I never enable blocking before a tuning baseline exists.
