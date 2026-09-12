<!--
reps: 0
priority: 0
-->
#Security/CICD #DevOps/CICD #SRS

# What is DevSecOps

> [!abstract] Short answer
> DevSecOps is the practice of **building security into the DevOps pipeline itself** - shared ownership, automated checks at every stage, and fast feedback - instead of a security review gate at the end. The referenceable engineering definition is NIST SP 800-218, the Secure Software Development Framework (SSDF), which groups the core practices into four families: **Prepare the Organization (PO), Protect the Software (PS), Produce Well-Secured Software (PW), and Respond to Vulnerabilities (RV)**.

## What changes operationally

```d2
direction: right
code: "Design + code\nthreat-model, secure standards" { width: 240; height: 90; style.fill: "#e3f2fd"
ci: "CI\nSAST, SCA, secrets scan" { width: 200; height: 90; style.fill: "#fff3e0"
test: "Test env\nDAST, dependency, IaC checks" { width: 250; height: 90; style.fill: "#fff3e0"
rel: "Release\nSBOM, signing, provenance" { width: 220; height: 90; style.fill: "#e8f5e9"
ops: "Operate\nmonitoring, vuln response" { width: 220; height: 90; style.fill: "#e8f5e9"
code -> ci -> test -> rel -> ops
```

**Fig. 1.** Security checks distributed along the pipeline rather than a gate before release; every stage's output feeds the next stage's defenses ([[What is the difference between SAST and DAST]] and [[What is an SBOM]] live here).

The SSDF's four groups in engineering terms:

- **Prepare the Organization**: defined roles and tooling for secure development, training, and requirements that include security - the "whose job is this" answer (everyone's, with named owners).
- **Protect the Software**: version control for all code, verified provenance, access control on build systems, integrity of the pipeline itself - the CI/CD estate is production infrastructure ([[How do you manage secrets in CI CD pipelines]]).
- **Produce Well-Secured Software**: the development core - minimal components with checked provenance (PW.4), compiler warnings and secure-compiler flags, code review **and code analysis** (PW.7.2), plus executable-code testing for "vulnerabilities not identified by previous reviews, analysis, or testing" (PW.8.1).
- **Respond to Vulnerabilities**: intake and disclosure process, triage, remediation - vulnerability management as a defined capability ([[What is the difference between CVE and CVSS]] in its natural habitat).

## Why it is a culture shift, not a tool purchase

The DevOps contract is fast, frequent, automated delivery; bolting a security review on the end either slows delivery until security is bypassed or rubber-stamps everything. DevSecOps moves the decision points into the automated path - policy-as-code, scanner gates tuned to be actionable, security review by exception - so the secure path is the fast path. The SSDF's framing ("organizations should...") exists so buyers and auditors can verify the practice, which is why US federal software requirements adopted it as the checkable baseline.

> [!warning] "We run a SAST scanner, so we do DevSecOps"
> A scanner in CI is one practice from one group (PW.7). The framework's substance is elsewhere: protected build systems, provenance and SBOM, defined vulnerability response, trained people - and tuned gates that developers actually work with rather than suppress. A pipeline that blocks every build on raw scanner output teaches the team to ignore or disable security; that is the opposite of the intent ([[What is the OWASP Top 10]] is the risk vocabulary the gates encode).

> [!tip] Interview answer
> DevSecOps integrates security into the pipeline with shared ownership - the checkable definition is NIST SP 800-218's SSDF: prepare the organization, protect the software, produce well-secured software, respond to vulnerabilities. Concretely: SAST/SCA/secrets scans in CI, DAST and IaC checks on the way to release, SBOM and provenance out, vulnerability response as a process - and gates tuned so the secure path stays the fast path.
