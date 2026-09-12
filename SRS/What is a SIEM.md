<!--
reps: 0
priority: 0
-->
#Security/BlueTeam #SRS

# What is a SIEM

> [!abstract] Short answer
> A SIEM (Security Information and Event Management) is the centralized platform that **collects logs and events from across the estate, normalizes and correlates them, and raises alerts**. NIST SP 800-61 places it next to IDPS products - "similar to IDPS products, but they generate alerts based on analysis of log data" - which is the crisp version: an IDPS watches traffic, a SIEM watches *what everything else recorded*.

## The pipeline

```d2
direction: right
src: "Sources\nhosts, firewall, IDPS, apps, cloud, IdP" { width: 300; height: 90; style.fill: "#e3f2fd"
col: "Collection + normalization\nparsers, time sync" { width: 260; height: 90; style.fill: "#fff3e0"
cor: "Correlation + rules\nmatches across sources" { width: 240; height: 90; style.fill: "#fff3e0"
al: "Alerts -> SOC triage\n(+ dashboards, reports)" { width: 250; height: 90; style.fill: "#ffebee"
src -> col -> cor -> al
```

**Fig. 1.** The SIEM as the hub of detection: value comes from cross-source correlation - one login event is noise; that login followed by mass file reads and an outbound transfer is an incident.

- **Ingest**: firewalls, IDPS ([[What is the difference between IDS and IPS]]), endpoint agents, application and web-server logs, authentication servers, cloud audit trails - ship by agent, syslog, or streaming integration.
- **Normalize**: everything parsed into common schemas (fields for user, host, IP, action); NTP-disciplined timestamps, since correlation is worthless without a shared clock.
- **Correlate and alert**: rules (brute-force patterns, impossible travel, privileged-role anomalies), increasingly plus behavioral analytics (UEBA) and SOAR hooks that automate playbooks.
- **Retain**: searchable retention sized to policy and forensics needs - "how was the breach done in March" is answered from here months later.

## The role in incident response

SP 800-61's detection phase leans on "sources of precursors and indicators" - and the SIEM is where most of those sources converge: it is the tool an analyst queries to scope an incident (which accounts, which hosts, what timeline) and the recorder that feeds post-incident lessons ([[What is the incident response lifecycle]]).

> [!warning] "We bought a SIEM, so we detect threats"
> An unturned SIEM produces either silence or a flood - both look identical to a team that stopped reading. Detection quality lives in rule tuning against real data, log coverage of what actually matters (identity and admin paths first), and staffed triage; the platform is the least important of the three. Garbage logs in, garbage alerts out - and missing time sync silently destroys every correlation ([[What is a blue team]] runs on this tooling, not instead of it).

> [!tip] Interview answer
> A SIEM centralizes logs and events, normalizes them, correlates across sources, and alerts - NIST's line is that it is like an IDPS but working on log data rather than traffic. I judge a SIEM deployment by coverage of identity and admin paths, clock discipline, rule tuning, and retention - the platform itself is the cheap part.
