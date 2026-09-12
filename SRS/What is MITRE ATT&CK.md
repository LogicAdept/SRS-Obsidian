<!--
reps: 0
priority: 0
-->
#Security/ThreatIntelligence #SRS

# What is MITRE ATT&CK

> [!abstract] Short answer
> MITRE ATT&CK is a **globally accessible knowledge base of adversary tactics and techniques based on real-world observations** - MITRE's own description. It organizes the field as tactics (the adversary's *why*: Initial Access through Impact) crossed with techniques (the *how*: documented behaviors like phishing or credential dumping), each with sub-techniques, procedures, and detected real-world group usage. Free and open, it is the shared map for detections, adversary emulation, and incident analysis.

## The structure

```d2
direction: right
ta: "Tactics (columns)\nInitial Access, Persistence,\nLateral Movement, Exfiltration..." { width: 320; height: 100; style.fill: "#e3f2fd"
te: "Techniques / sub-techniques\nT1566 Phishing -> .004 Spearphishing Link" { width: 320; height: 100; style.fill: "#fff3e0"
pr: "Procedures\nhow observed groups used it" { width: 260; height: 90; style.fill: "#e8f5e9"
ta -> te -> pr
```

**Fig. 1.** The knowledge base as a grid: tactic = objective at that stage, technique = the behavioral way of achieving it, procedure = the concrete instance an observed group used.

- **Matrices**: Enterprise (the main one - endpoints, cloud, identity), Mobile, and ICS; each technique page carries detection guidance, mitigation pointers, data-source notes, and procedure examples from tracked groups and campaigns.
- **Why behavior, not tools**: malware hashes and C2 domains change per campaign ([[What is threat intelligence]]'s rotting IoCs); "OS Credential Dumping via LSASS memory" describes a behavior that survives recompilation - which is why detections anchored to behaviors outlast detections anchored to samples.
- **Uses**: mapping current detections against techniques to find coverage gaps; planning adversary emulation for [[What is the difference between a penetration test and a red team exercise]]; normalizing incident write-ups ([[What is the incident response lifecycle]] reports in ATT&CK language); threat-informed prioritization with derived scores.

> [!warning] "We are 70% covered against ATT&CK"
> Coverage percentages are easy to inflate: a control that "touches" a technique is not a detection of it, and vendor dashboards count differently than your telemetry does. ATT&CK has no certification and no maturity model by design - it is a common language; the defensible version of this work maps techniques to *specific, tested* detections in your own stack, purple-team style ([[What is a blue team]] owns that loop).

> [!tip] Interview answer
> ATT&CK is MITRE's free knowledge base of adversary tactics and techniques built from real-world observation - tactics as columns from Initial Access to Impact, techniques as documented behaviors with procedures from tracked groups, published as Enterprise, Mobile, and ICS matrices. I use it as the shared map for detection coverage, emulation planning, and incident reporting - as a language, not a certification.
