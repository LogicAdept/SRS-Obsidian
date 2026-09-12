<!--
reps: 0
priority: 0
-->
#Security/ThreatIntelligence #SRS

# What is the difference between CVE and CVSS

> [!abstract] Short answer
> CVE is the **name**; CVSS is the **score**. A CVE ID is a universal identifier for one publicly known vulnerability - NIST SP 800-94 calls CVE numbers "universal identifiers for vulnerabilities", and SP 800-115 describes CVE as a list of standardized names for known vulnerabilities. CVSS (maintained by FIRST) is the scoring system that grades severity from 0 to 10; the NVD enriches CVE entries with CVSS scores. Vulnerability scanners, advisories, and SBOM tooling speak both: the ID tells you *which* flaw, the score tells you *how bad by default*.

## The two halves of one report

```d2
direction: right
cve: "CVE-2024-XXXXX\nwhich vulnerability" { width: 240; height: 80; style.fill: "#e3f2fd"
nvd: "NVD entry\ndescription, affected versions, refs" { width: 300; height: 90; style.fill: "#fff3e0"
cvss: "CVSS base score\nhow severe by default" { width: 250; height: 80; style.fill: "#ffebee"
cve -> nvd -> cvss
```

**Fig. 1.** The pipeline from identifier to scored record. "CVE-2024-12345 has CVSS 9.8" is two different claims sharing one sentence.

## CVSS v3.1 in the detail that matters

The **Base metric group** scores intrinsic characteristics "constant over time and across user environments" (FIRST CVSS v3.1 specification):

- **Exploitability** - Attack Vector (Network / Adjacent / Local / Physical: "the more remote... the greater the Base Score"), Attack Complexity, Privileges Required, User Interaction;
- **Impact** - Confidentiality / Integrity / Availability impact on the vulnerable component, plus **Scope** (does a successful exploit affect resources beyond the vulnerable component's security scope);
- the combination yields the familiar 0-10 score and severity bands: Low 0.1-3.9, Medium 4.0-6.9, High 7.0-8.9, Critical 9.0-10.0.

Two more metric groups adjust the base: **Temporal** (exploit code exists? official fix available?) and **Environmental** (your asset's importance) - rarely published but exactly where "9.8 everywhere" becomes honest risk.

## How they work together in practice

A scanner finds component X at version Y -> matches it to a CVE ID via the NVD -> surfaces the CVSS base score -> your triage decides. For prioritization beyond the default score, the missing context is yours: exploit availability, exposure, compensating controls - the environmental judgment CVSS cannot make for you ([[What is an SBOM]] is what makes the matching step systematic; [[What is the difference between SAST and DAST]] covers the code-level half of finding these first).

> [!warning] "CVSS 9.8 means fix it first"
> The base score knows nothing about your deployment: an "unauthenticated remote RCE" (critical base) on an air-gapped internal tool is a different risk than the same CVE on an internet-facing gateway - exploit maturity and reachability are Temporal/Environmental concerns the published 9.8 does not carry. Prioritizing purely by base score burns scarce fixes on unreachable flaws while reachable mediums wait ([[What is the OWASP Top 10]] ordering has the same caution label - awareness, not triage).

> [!tip] Interview answer
> CVE is the identifier - a universal name for one known vulnerability, per NIST's own descriptions - while CVSS is FIRST's severity scoring: base metrics over exploitability and impact giving 0-10, with temporal and environmental groups for context. The NVD glues them: CVE entry, CVSS score attached. And I never triage by base score alone - exposure and exploit maturity are the environmental half of the decision.
