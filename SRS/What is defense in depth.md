<!--
reps: 0
priority: 0
-->
#Security/BlueTeam #SRS

# What is defense in depth

> [!abstract] Short answer
> Defense in depth layers independent controls so that **no single failure is a compromise**: an attacker must beat network controls, then host hardening, then application checks, then data protections. NIST SP 800-41 frames it directly - a firewall is a first line, not the whole line, and organizations should practice defense in depth "in which layers of firewalls and other security systems are used throughout the network" rather than depending on any single device.

## The layers and the point of them

```d2
direction: right
l1: "Perimeter\nfirewall, WAF" { width: 190; height: 70; style.fill: "#e3f2fd"
l2: "Network\nsegmentation" { width: 180; height: 70; style.fill: "#e3f2fd"
l3: "Host\npatching, non-root" { width: 190; height: 70; style.fill: "#fff3e0"
l4: "Application\ninput validation, authz" { width: 220; height: 70; style.fill: "#fff3e0"
l5: "Data\nencryption, least privilege" { width: 210; height: 70; style.fill: "#e8f5e9"
l1 -> l2 -> l3 -> l4 -> l5
```

**Fig. 1.** Layered controls, each assumed to fail independently. The design goal is that the layers are *diverse* - one bug class should not defeat two layers at once.

- **Perimeter**: firewalls, WAF ([[What is a WAF]]) - buys time and drops the loud attacks.
- **Network**: segmentation and DMZ so a foothold cannot walk ([[What is network segmentation]], [[What is a DMZ in network security]]).
- **Host**: patch discipline, non-root services, minimal packages ([[How do you run a Docker container as a non-root user]]).
- **Application**: parameterized queries, output encoding, object-level authorization ([[How would you explain SQL injection attacks and defenses]], [[How would you explain IDOR]]).
- **Data**: encryption at rest/in transit, scoped DB grants - so even a read of storage is not a read of data ([[What is the principle of least privilege]]).
- **Detection and response**: IDPS, SIEM, incident response - the layer that assumes an attacker is present ([[What is the difference between IDS and IPS]], [[What is the incident response lifecycle]]).

## Why "we have a firewall" is not depth

Depth is measured against failure: if the perimeter control misses (0-day, misconfiguration, insider, phishing), which independent control notices, slows, or stops the next step? Depth also distributes **responsibility for the same risk across controls** - SQLi is partly prevented by validation, partly by parameterization, partly limited by DB grants, partly detected by query logging - so each individual control may be imperfect without the data being lost.

> [!warning] "More layers automatically means more secure"
> Layers interact: duplicated controls share bugs (same parser, same config error), stacked rules produce false confidence and operational friction, and security debt accumulates in what nobody can reason about anymore. The discipline is *independent, tested* layers - verified by attack-path walkthroughs, not by counting boxes in the diagram ([[What is zero trust architecture]] is the modern architecture-level restatement of the same idea).

> [!tip] Interview answer
> Defense in depth stacks independent controls - perimeter, segmentation, host, application, data, plus detection - so one failure is not a breach, and I mean independence: diverse mechanisms that fail separately, each assumed broken. The firewall stops the loud, segmentation stops the walk, app-layer checks stop the exploit, encryption and least privilege limit what a breach reads.
