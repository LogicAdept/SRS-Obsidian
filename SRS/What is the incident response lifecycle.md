<!--
reps: 0
priority: 0
-->
#Security/BlueTeam #SRS

# What is the incident response lifecycle

> [!abstract] Short answer
> NIST SP 800-61 organizes incident handling into four phases - **Preparation; Detection and Analysis; Containment, Eradication, and Recovery; Post-Incident Activity** - drawn as a cycle with feedback arrows: lessons from every incident feed back into preparation. The loop is not a waterfall; real incidents oscillate between phases as analysis deepens and new indicators appear.

## The four phases

```d2
direction: right
p: "1. Preparation\npolicy, playbooks, tools, training" { width: 300; height: 90; style.fill: "#e3f2fd"
d: "2. Detection and Analysis\nprecursors and indicators, triage, scope" { width: 320; height: 90; style.fill: "#fff3e0"
c: "3. Containment, Eradication,\nRecovery\nstop spread, remove, restore" { width: 320; height: 100; style.fill: "#ffebee"
po: "4. Post-Incident Activity\nlessons learned -> playbooks" { width: 300; height: 90; style.fill: "#e8f5e9"
p -> d -> c -> po -> p: "feedback"
```

**Fig. 1.** The SP 800-61 cycle (Figure 3-1). The closing arrow is the one organizations skip - and the reason the same incident repeats with different filenames.

- **Preparation**: incident response capability *and* prevention - policy, contact trees, playbooks, logging and retention ([[What is a SIEM]] as the data backbone), tooling, exercises. The phase where everything later either exists or does not.
- **Detection and Analysis**: collect precursors and indicators from SIEM, IDPS, antivirus, admins and users; triage to decide "is this an incident, and which incident"; scope it - accounts, hosts, timeline - before acting.
- **Containment, Eradication, and Recovery**: pick a containment strategy (isolate hosts, block accounts, sinkhole C2) balancing evidence preservation against damage; eradicate (remove persistence, close the entry vector); recover (restore from clean backups, verify, monitor for re-infection).
- **Post-Incident Activity**: the lessons-learned meeting within weeks, evidence-driven answers to what happened and how, updated playbooks, controls, and detections.

## The judgment calls the guide highlights

Containment strategy is explicitly a tradeoff - SP 800-61 lists factors like attacker sophistication, evidence volatility, service availability, and duration of the compromise; pulling the plug on a compromised payment host preserves evidence but stops the business. Evidence handling runs through all phases: acquisition and chain of custody decide whether anything learned survives legal or HR review.

> [!warning] "We contain first, ask questions later"
> Wiping the host kills the answer to "how did they get in" - and without it, eradication is theater because the entry vector remains. The mirror error is analysis paralysis: a team that only documents while the attacker moves laterally. The lifecycle exists precisely because both halves matter - contain with evidence, learn with urgency ([[What is a blue team]] rehearses these calls in exercises before real ones).

> [!tip] Interview answer
> NIST SP 800-61's four phases: preparation, detection and analysis, containment-eradication-recovery, and post-incident activity, looping back into preparation. The craft is in the judgment calls - scoping before acting, containment strategy that preserves evidence, lessons learned that actually change playbooks - and the phase teams skip is always the last one.
