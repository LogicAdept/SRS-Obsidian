<!--
reps: 0
priority: 0
-->
#Security/BlueTeam #SRS

# What is a blue team

> [!abstract] Short answer
> The blue team is the **defending side**: NIST's glossary (CNSSI 4009) defines it as "the group responsible for defending an enterprise's use of information systems by maintaining its security posture" against mock attackers, defending "over a significant period of time" in a representative operational context under white-team rules. In practice: SOC analysts, detection engineering, threat hunting, hardening, and incident response - the people the red team is measured against.

## What the blue team actually does

- **Monitor**: watch SIEM/EDR telemetry, triage alerts, separate signal from noise around the clock ([[What is a SIEM]]).
- **Detect**: write and tune detections - correlation rules, behavioral analytics, hunt hypotheses - mapped to adversary behavior ([[What is MITRE ATT&CK]] is the shared map).
- **Respond**: run the incident response lifecycle end to end ([[What is the incident response lifecycle]]).
- **Harden**: close the gaps exercises and incidents reveal - patching baselines, segmentation fixes, identity hygiene ([[What is defense in depth]] is the blueprint they maintain).
- **Learn adversarially**: purple-team sessions with the red team - replay attacks jointly, verify each detection fires, tune, repeat ([[What is the difference between a penetration test and a red team exercise]] explains the offensive side).

```d2
direction: right
rt: "Red Team\nemulates adversary" { width: 210; height: 80; style.fill: "#ffebee"
bt: "Blue Team\nmonitors, detects, responds" { width: 240; height: 80; style.fill: "#e8f5e9"
wt: "White Team\nrules, refereeing" { width: 190; height: 70; style.fill: "#e3f2fd"
pt: "Purple Team\njoint tuning loop" { width: 210; height: 70; style.fill: "#fff3e0"
rt -> pt
pt -> bt
wt -> rt
wt -> bt
```

**Fig. 1.** The exercise roles from the CNSS model: red attacks, blue defends over time, white referees - and the purple-team loop turns both sides' work into better detections.

## The glossary conditions carry the meaning

The definition's three clauses are the substance: "significant period of time" (a defense is evaluated across days, not a single snapshot), "representative operational context" (real tooling, real telemetry - not a slide exercise), and "rules established and monitored with the help of a neutral group" (white team keeps exercises honest and bounded). Together they describe why blue-teaming is a *capability*, not an assignment: it presumes monitoring exists, detections are testable, and response is practiced.

> [!warning] "Blue team is just who answers the alert queue"
> Alert triage is one function. A team that only reacts is understaffed by definition - detection engineering, hunting, and hardening are proactive blue-team work, and the difference between a struggling and a mature defense is usually how much of the time goes into those rather than into chasing noise. And no, a blue team is not a product you can buy - EDR is a tool the team operates.

> [!tip] Interview answer
> Blue team is the defense side per the CNSS/NIST definition - maintaining security posture against emulated attackers over time, under white-team rules. Day to day that is SOC monitoring and triage, detection engineering mapped to ATT&CK, threat hunting, hardening, and incident response, plus purple-team loops where red's techniques become tuned detections.
