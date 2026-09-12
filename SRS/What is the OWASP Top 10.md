<!--
reps: 0
priority: 0
-->
#Security/AppSec/OWASP #SRS

# What is the OWASP Top 10

> [!abstract] Short answer
> The OWASP Top 10 is the OWASP Foundation's consensus **awareness document**: the ten most critical security risk classes for web applications, refreshed from contribution and survey data. The current edition is **Top 10:2025** - A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions.

## The 2025 list and what moved

```text
A01  Broken Access Control
A02  Security Misconfiguration
A03  Software Supply Chain Failures
A04  Cryptographic Failures
A05  Injection
A06  Insecure Design
A07  Authentication Failures
A08  Software or Data Integrity Failures
A09  Security Logging and Alerting Failures
A10  Mishandling of Exceptional Conditions
```

**Listing 1.** Top 10:2025. Supply-chain failures rose to A03, and A10 (mishandling of exceptional conditions) is new to the list; the logging entry is now explicitly "logging and alerting". Categories are **risk classes** - Injection spans SQL, command, and template injection; it is not one bug.

## How the document is meant to be used

- **Prioritization**: it says "start here" for awareness and program building - access control, misconfiguration, and supply chain dominate real-world findings ([[How would you explain IDOR]] lives in A01; [[What is SSRF]] in the server-side request class; [[How would you explain SQL injection attacks and defenses]] in A05).
- **Not a test plan**: "we checked ten things" is not an assessment - OWASP's ASVS provides the depth checklist; the Top 10 is the awareness layer above it.
- **Shared vocabulary**: it gives a team and its auditors names for classes, so tickets and reviews refer to the same risk rather than to individual payloads.
- **Historical continuity**: since 2003 the list has tracked how the web's risk mass moved - injection and broken access control dominated for years, while 2025's rise of supply-chain failures reflects build pipelines and dependencies becoming the preferred entry point ([[What is an SBOM]] is the countermeasure the movement produced).

> [!warning] "We are compliant because we scanned for the Top 10"
> Two distortions at once: the Top 10 is not a scanner signature set, and categories like Insecure Design or Mishandling of Exceptional Conditions are not detectable by a payload list at all. It is an awareness ranking built from incident and contributor data - the mapping to your architecture needs a human ([[What is DevSecOps]] is the practice that turns it into pipeline checks).

> [!tip] Interview answer
> The OWASP Top 10 is OWASP's consensus list of the most critical web application risk classes - the 2025 edition runs from Broken Access Control and Security Misconfiguration through Supply Chain Failures and Injection to the new Mishandling of Exceptional Conditions. I use it as a prioritization and vocabulary layer, with ASVS as the actual depth checklist behind it.
