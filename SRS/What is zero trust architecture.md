<!--
reps: 0
priority: 0
-->
#Security/NetworkSecurity #SRS

# What is zero trust architecture

> [!abstract] Short answer
> Zero trust removes **implicit trust based on network location**: NIST SP 800-207 defines a ZTA where every access request is authenticated, authorized per session against dynamic policy (identity, device state, behavior), and enforced through a policy engine and enforcement point - no matter whether the source sits in the office, the VPN, or the same subnet. Its seven tenets start with "all data sources and computing services are resources" and "all communication is secured regardless of network location".

## The tenets in compressed form

SP 800-207 states seven basic tenets:

1. All data sources and computing services are **resources**.
2. **All communication is secured** regardless of network location - being "inside" grants nothing.
3. Access to individual resources is granted **per session**, least privilege ([[What is the principle of least privilege]]).
4. Access is decided by **dynamic policy** - client identity, application, requesting-asset state, behavioral and environmental attributes.
5. The enterprise **monitors and measures** the integrity and security posture of all owned assets.
6. Authentication and authorization are **dynamic and strictly enforced** before access, continuously re-evaluated.
7. The enterprise collects as much information as possible about assets, infrastructure, and communications - to improve posture.

```d2
direction: right
s: "Subject\nuser + device" { width: 190; height: 70; style.fill: "#e3f2fd"
pep: "PEP\npolicy enforcement point" { width: 220; height: 80; style.fill: "#fff3e0"
pdp: "PDP\npolicy engine + info" { width: 220; height: 80; style.fill: "#e8f5e9"
r: "Resource" { width: 150; height: 60; style.fill: "#e8f5e9"
s -> pep -> r
pep -> pdp: "evaluate each session"
pdp -> pep: "allow / deny + context"
```

**Fig. 1.** The logical core: the enforcement point never decides alone; the policy decision point evaluates identity, asset posture, and context per session.

## Approaches and where they appear

SP 800-207 groups ZTA deployments into three approaches - **enhanced identity governance** (policy centered on identity and attributes), **micro-segmentation** (per-resource or per-workload gateways, the [[What is network segmentation]] idea pushed to individual workloads), and **network infrastructure / software defined perimeters** (the controller assembles on-demand connections instead of exposing a flat network). A ZTA complements, not replaces, existing perimeter controls - 800-207 is explicit that pure-form tenets are an ideal, rarely fully implementable.

> [!warning] "Zero trust is a product you can buy"
> It is an architecture and a policy model - vendors sell components (identity-aware proxies, device posture agents, SDP controllers), but "deployed VPN replacement X" is not zero trust if any decision still says "source IP is internal, allow". The second classic misreading is "no firewalls anymore" - 800-207 keeps them as one layer; what dies is *implicit* trust, not controls ([[What is a DMZ in network security]] remains useful hardening).

> [!tip] Interview answer
> Zero trust is NIST SP 800-207's model: no implicit trust from network position - every session is authenticated, authorized against dynamic policy (identity, device posture, behavior), and enforced via PDP/PEP. It deploys as identity governance, micro-segmentation, or SDP, complements the perimeter rather than deleting it, and the honest caveat is that its seven tenets are an ideal few enterprises fully reach.
