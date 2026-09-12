<!--
reps: 0
priority: 0
-->
#Security/Compliance #SRS

# What is PCI DSS

> [!abstract] Short answer
> PCI DSS (Payment Card Industry Data Security Standard) is the card-industry's mandatory security standard for everyone who **stores, processes, or transmits cardholder data (CHD) or sensitive authentication data (SAD)**, or "could impact the security of the cardholder data environment (CDE)" - the PCI SSC's own scope wording, covering merchants, processors, acquirers, issuers, and service providers. Its sharpest engineering rules: sensitive authentication data (CVV/CVC, full track data, PIN blocks) **must not be stored after authorization at all**, PAN must be unreadable where stored and **masked to at most the first six and last four digits when displayed**, and logs must not carry full PAN.

## The non-negotiables engineers meet

```d2
direction: right
in: "Card data in\nfrom payment channels" { width: 230; height: 80; style.fill: "#e3f2fd"
app: "Your systems in CDE\nstorage, processing, transmission" { width: 280; height: 90; style.fill: "#fff3e0"
sad: "SAD: CVV, track, PIN\nNOT stored post-auth - even encrypted" { width: 320; height: 90; style.fill: "#ffebee"
pan: "PAN: encrypt at rest,\nmask display (first 6 + last 4)" { width: 320; height: 90; style.fill: "#e8f5e9"
in -> app -> sad
in -> app -> pan
```

**Fig. 1.** The data-classification line that decides most designs: CHD (primarily the PAN) can be stored under heavy controls; sensitive authentication data cannot be stored at all after the authorization response.

- **No SAD retention**: CVV2/CVC2 must not be stored *even encrypted* after authorization; track data and PIN blocks likewise. Most payment integrations exist precisely to outsource this problem to a tokenization provider.
- **PAN protection**: encryption or truncation/hashing at rest; display masked (first six, last four maximum per the v4 rules); no full PAN in application logs, debug output, or URLs - and log ingestion is reviewed for it ([[What is PII]]'s masking discipline, with harder rules).
- **The standard's twelve requirement families**: network security controls, secure defaults, CHD protection, vulnerability management, access control (unique IDs, least privilege, MFA), monitoring/testing of networks, information security policy - the familiar "build and maintain / protect / maintain / regularly monitor / test" structure.
- **Validation**: annual assessment (QSA ROC or self-assessment AOC by merchant level), quarterly ASV scans of public ranges; compliance is attested per entity, and card brands enforce it contractually.

## The architectural consequence

The cheapest way to comply is to **not touch card data**: hosted payment fields, tokenization, and third-party processors shrink the CDE - and segmentation ([[What is network segmentation]]) is what keeps a declared scope honest by proving non-CDE systems cannot reach it. A flat network forces the whole estate into scope; a segmented one pays for controls only where card data actually flows.

> [!warning] "We are too small for PCI DSS"
> Scope follows the data, not the company size - any entity storing, processing, or transmitting CHD (or impacting the CDE) is in scope, with lighter *validation* for smaller merchants but the same storage prohibitions. The second classic: "we tokenize, so PCI is done" - a misconfigured integration that logs tokens with PAN fragments or stores SAD during retries puts you right back in scope. And compliance is a floor: passing the assessment is not the same as being secure ([[What is the OWASP Top 10]] is the engineering view of the same risks).

> [!tip] Interview answer
> PCI DSS is the card-industry standard binding anyone who stores, processes, or transmits cardholder data - or can impact the CDE. The engineering rules I quote: never store sensitive authentication data after authorization, even encrypted; encrypt and mask PAN to first-six/last-four; keep full PAN out of logs. Best design is not touching card data at all - tokenization and segmentation shrink the scope you have to defend and audit.
