<!--
reps: 0
priority: 0
-->
#Security/NetworkSecurity #SRS

# What is network segmentation

> [!abstract] Short answer
> Network segmentation divides a flat network into isolated zones - subnets, VLANs, firewall-enforced segments, or per-workload micro-segments - so traffic between zones is filtered and **lateral movement** after a single compromise is limited. A DMZ is one segment of this design; PCI DSS's cardholder-data-environment scoping and NIST SP 800-207's micro-segmentation are the same principle at compliance and zero-trust granularity.

## What segmentation buys

- **Blast radius**: a phished laptop in the office VLAN cannot reach the database tier; a compromised build server cannot browse the production VPC. East-west traffic (server to server, workload to workload) is where attackers move - segmentation is what turns "one host down" into "one host down" instead of "the datacenter is one domain".
- **Scope reduction**: compliance scope follows reachability - the PCI DSS cardholder environment shrinks to the segments that actually touch card data, and the audit scope shrinks with it ([[What is PCI DSS]]).
- **Policy per zone**: internet-facing, internal app, data, management, and build segments each get their own rule set - which is how least privilege becomes enforceable at network level ([[What is the principle of least privilege]]).

```d2
direction: right
edge: "Edge / DMZ" { width: 170; height: 70; style.fill: "#fff3e0"
app: "App tier" { width: 150; height: 70; style.fill: "#e3f2fd"
data: "Data tier\nDBs only from app tier" { width: 240; height: 80; style.fill: "#e8f5e9"
mgmt: "Mgmt / build\nno direct prod reach" { width: 240; height: 80; style.fill: "#ffebee"
edge -> app -> data
mgmt -x data
```

**Fig. 1.** Tiered segmentation: each tier accepts traffic only from the tier that needs it; build and management networks do not ride production routes.

## Enforcement points

- **Subnet + router ACLs / firewalls** between zones - the classic layered model (NIST SP 800-41's layered firewall strategy is the perimeter-scale version).
- **VLANs** separate broadcast domains - real isolation only where inter-VLAN routing is filtered; a "segmented" network whose router forwards everything is one big segment with extra steps.
- **Micro-segmentation**: policy per workload (host firewall, SDN, service mesh, distributed firewall), the zero-trust deployment shape - NIST SP 800-207 lists it as one of the canonical ZTA approaches, replacing "inside = trusted" with per-flow decisions ([[What is zero trust architecture]]).

> [!warning] "We have VLANs, so we are segmented"
> VLAN separation without filtered routing, shared management planes, or one flat "trusted" zone behind the firewall gives you addressing hygiene, not containment - attackers pivot through whatever routes exist. Segmentation is defined by what the *rules* forbid, not by how many broadcast domains exist ([[What is the difference between IDS and IPS]] adds the detection layer on top).

> [!tip] Interview answer
> Segmentation chops the network into zones with filtered inter-zone traffic so a single compromise stops moving laterally: DMZ, app, data, management, build - and per-workload micro-segmentation when we want zero-trust granularity. VLANs alone are not it; the enforcement is the routing and firewall policy between the segments, and compliance scope reduction is often the business case.
