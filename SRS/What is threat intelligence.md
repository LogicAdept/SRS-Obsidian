<!--
reps: 0
priority: 0
-->
#Security/ThreatIntelligence #SRS

# What is threat intelligence

> [!abstract] Short answer
> Threat intelligence is **processed knowledge about adversaries that a defender can act on**. NIST SP 800-150 defines cyber threat information as "any information that can help an organization identify, assess, monitor, and respond to cyber threats" - concretely: indicators of compromise (system artifacts or observables associated with an attack), adversary TTPs, security alerts, threat intelligence reports, and recommended tool configurations. The discipline turns that raw material into decisions: block, detect, prioritize, or investigate.

## The content ladder

```d2
direction: right
ioc: "Indicators\nIPs, hashes, domains, artifacts" { width: 250; height: 80; style.fill: "#e3f2fd"
ttp: "TTPs\nhow the adversary operates" { width: 220; height: 80; style.fill: "#fff3e0"
ctx: "Campaign / actor context\nwho, why, targeting" { width: 250; height: 80; style.fill: "#e8f5e9"
act: "Action\nblock, detect, hunt, prioritize" { width: 250; height: 80; style.fill: "#ffebee"
ioc -> ttp -> ctx -> act
```

**Fig. 1.** Rising value and durability: an IP address rots in days, a TTP ("signed driver abuse for persistence") stays true across campaigns, and context decides where defenses go.

- **Indicators of compromise (IoCs)**: the atomic layer - hashes, IPs, domains, mutexes, artifacts. Fast to consume, fast to rot; SP 800-150's "system artifacts or observables associated with an attack".
- **TTPs**: tactics, techniques, and procedures - the behavioral layer that survives infrastructure churn; this is the level [[What is MITRE ATT&CK]] catalogs.
- **Reports and context**: campaign analysis, actor attribution, targeting assessment - the layer that informs leadership and architecture, not just blocklists.
- **Sharing**: the SP 800-150 thesis - organizations that share threat information "improve their own security postures as well as those of other organizations"; structured exchange rides standards (STIX for representation, TAXII for transport).

## Consumption - where intelligence becomes security

- **Automated**: IoC feeds into firewalls, proxies, and [[What is a SIEM]] correlation; scoring and expiry attached, because yesterday's C2 address is noise today.
- **Analytical**: hunt hypotheses from TTPs ("if they persist via scheduled tasks, what would that look like in our telemetry?"); [[What is the difference between a penetration test and a red team exercise]] adversaries emulate exactly those TTPs.
- **Strategic**: prioritization input - which threats matter for your sector changes roadmap and hardening order.

> [!warning] "We subscribed to feeds, so we have threat intelligence"
> Raw feeds are inputs, not intelligence - without validation, context, expiry, and integration into detection and response they are a stream of false positives and stale IPs. The classic failure is blocking IoCs directly from low-trust feeds and taking down legitimate services; SP 800-150's whole emphasis is on the *process* - goals, handling, sharing relationships - not on the data volume ([[What is the difference between CVE and CVSS]] is the analogous discipline for the vulnerability half of the house).

> [!tip] Interview answer
> Threat intelligence turns adversary knowledge into decisions - SP 800-150's cyber threat information: IoCs, TTPs, alerts, reports, tooling advice. Value climbs from atomic indicators (fast, rots) through TTPs (durable, hunt-ready) to campaign context; sharing via STIX/TAXII multiplies everyone's posture. It becomes intelligence only when it changes blocking, detection, or priorities - a feed subscription by itself changes nothing.
