<!--
reps: 0
priority: 0
-->
#Security/CICD #SRS

# What is the difference between SAST and DAST

> [!abstract] Short answer
> SAST (static application security testing) analyzes **source or bytecode without running it** - it sees the code paths, data flows, and hardcoded secrets from the inside; DAST (dynamic application security testing) attacks a **running application from the outside** like a blind tester - probing endpoints, payloads, and configurations for what actually fires. They fail in opposite directions: SAST has false positives but full path coverage, DAST has high-confidence findings but only reaches what its crawler can touch - which is why they complement each other in a pipeline ([[What is DevSecOps]] wires them in).

## The two viewpoints

```d2
direction: right
s: "SAST\ninside: code, dataflow, secrets\npre-merge, language-aware" { width: 300; height: 100; style.fill: "#e3f2fd"
d: "DAST\noutside: running app, black box\nstaging, exploits fired for real" { width: 300; height: 100; style.fill: "#e8f5e9"
gap: "Neither covers:\nbusiness logic, design flaws" { width: 280; height: 80; style.fill: "#ffebee"
s -x gap
d -x gap
```

**Fig. 1.** Complementary blind spots - and the shared gap both leave for human review ([[What is the OWASP Top 10]]'s Insecure Design class lives exactly there).

- **SAST**: parses the codebase, taints user input through sinks, flags injection candidates, crypto misuse, and committed secrets. Runs at commit/PR time (minutes, incremental). Weaknesses: framework-blind guesses produce noise; needs suppression hygiene or it trains developers to dismiss findings; sees the code, not the runtime config.
- **DAST**: crawls and attacks the deployed application - injects [[How would you explain SQL injection attacks and defenses]] payloads, checks response-splitting and [[How would you explain XSS]] reflections, flags [[What is the difference between HTTP and HTTPS]]-level misconfigurations, missing headers, verbose errors. Findings are demonstrated against the real app, so confidence is high. Weaknesses: coverage is bounded by crawl depth and authentication; internal logic paths never exposed over HTTP are invisible.
- **Runtime-adjacent siblings**: SCA analyzes *dependencies* for known CVEs (the supply-chain half - [[What is the difference between CVE and CVSS]], [[What is an SBOM]]); IAST instruments the app during tests; both are frequently confused with SAST/DAST in vendor naming.

```yaml
- run: sast-scan --incremental        # PR gate: minutes, blocks on critical
- run: sca-scan --fail-on high        # dependency CVEs vs SBOM
- run: dast-scan --profile authed     # nightly on staging, crawled with a test account
```

**Listing 1.** Typical pipeline placement: SAST and SCA gate pull requests; DAST runs periodically on a deployed environment where a crawler can actually work.

> [!warning] "DAST found nothing, so the app is clean"
> A DAST pass is bounded by what its crawler reached and what its payloads match - authenticated flows, multi-step logic, and APIs behind session semantics routinely escape it. The inverse is equally wrong: SAST zero findings means the rules matched nothing, not that the code is safe - unscanned entry points, custom crypto, and suppression noise hide there. Both tools produce a floor, not a ceiling ([[What is penetration testing]] is the human layer above both).

> [!tip] Interview answer
> SAST reads code without running it - full path visibility, secrets and taint analysis, PR-time gate, noisy. DAST attacks the running app from outside - high-confidence, demonstrable findings, but only as far as its crawl reaches. SCA is the third sibling: dependency CVEs. None of them see business logic or design flaws, which is exactly why the pipeline runs SAST early and DAST on staging, and reviews close the gap.
