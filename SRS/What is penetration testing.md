<!--
reps: 0
priority: 0
-->
#Security/Pentest #SRS

# What is penetration testing

> [!abstract] Short answer
> A penetration test is an **authorized, time-boxed simulated attack** that verifies whether vulnerabilities are actually exploitable - and how far. NIST SP 800-115 organizes it into four phases: **Planning** (rules of engagement, approval, goals - "no actual testing occurs in this phase"), **Discovery** (scanning, enumeration, vulnerability analysis), **Attack** (exploiting confirmed vulnerabilities, escalating, pivoting - bounded by the ROE), and **Reporting** (findings, methodology, remediation).

## The four phases

```d2
direction: right
pl: "1. Planning\nROE, approval, goals" { width: 240; height: 90; style.fill: "#e3f2fd"
di: "2. Discovery\nscan, enumerate, analyze" { width: 250; height: 90; style.fill: "#fff3e0"
at: "3. Attack\nexploit, escalate, pivot" { width: 250; height: 90; style.fill: "#ffebee"
re: "4. Reporting\nfindings, risk, remediation" { width: 250; height: 90; style.fill: "#e8f5e9"
pl -> di -> at -> re
```

**Fig. 1.** The SP 800-115 phase model. The guide notes the grouping is one acceptable decomposition - the invariant is documented scope and rules before any attack activity.

What each phase produces:

- **Planning**: the rules of engagement - what is in scope, what must never be touched, test windows, escalation contacts, and the signed management approval that makes the whole thing legal rather than criminal.
- **Discovery**: asset and service enumeration plus vulnerability analysis - and the NIST-noted distinction that a *vulnerability* is only a candidate until exploited; the NVD's CVE/CVSS data feeds the analysis ([[What is the difference between CVE and CVSS]]).
- **Attack**: verify exploitability, attempt privilege escalation and lateral movement as the ROE permits - proving impact ("this web flaw yields the customer database") instead of guessing it ([[What is SSRF]] and [[How would you explain IDOR]] are classic web-app findings of this phase).
- **Reporting**: executive risk summary, detailed technical findings with reproduction steps, and prioritized remediation - the deliverable the whole exercise exists for.

## What it is and is not

A pentest answers "what can an attacker actually do" at a point in time - it complements, not replaces, code-level checks like SAST/DAST ([[What is the difference between SAST and DAST]]) and the continuous side of the practice ([[What is DevSecOps]]). Scope shapes it: network, web application, wireless, physical, or social engineering - and depth varies from black-box (no knowledge) to full white-box with source access.

> [!warning] "We passed a pentest, so we are secure"
> A pentest is a point-in-time sample under specific rules: it demonstrates what the testers found in the time they had, not the absence of vulnerabilities - and its findings start rotting with the next release. The mirror failure is treating the ROE as bureaucracy: testing without documented authorization is exactly how a paid engagement becomes an incident ([[What is the difference between a penetration test and a red team exercise]] covers when the broader, stealthier variant is warranted).

> [!tip] Interview answer
> Penetration testing is authorized simulated attack under a rules-of-engagement document - NIST SP 800-115's four phases: planning with no testing, discovery, attack to prove real exploitability, and reporting with prioritized fixes. It answers "what can an attacker actually achieve" point-in-time; it does not certify security, and its legality lives entirely in that signed scope.
