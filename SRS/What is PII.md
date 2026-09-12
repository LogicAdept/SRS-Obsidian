<!--
reps: 0
priority: 0
-->
#Security/Compliance #SRS

# What is PII

> [!abstract] Short answer
> PII (personally identifiable information) is NIST SP 800-122's term for **any information about an individual that distinguishes or traces their identity** - name, SSN, date and place of birth, biometrics - plus "any other information that is **linked or linkable** to an individual, such as medical, educational, financial, and employment information". The linkable half is the operative part: data becomes PII through combination, so log masking, minimization, and access control are the everyday defenses.

## Direct and linkable identifiers

| Direct identifiers | Linkable combinations |
|---|---|
| full name, SSN, passport number | ZIP code + birth date + gender |
| biometric records, card number | device ID + browsing history |
| email, phone | rare diagnosis + small town |

**Listing 1.** The 800-122 split: the left column is PII on its own; the right column becomes PII when joined - which is why dropping the name from a record does not de-identify it.

The engineering consequences of "linkable":

- **Logs are the usual leak**: stack traces and request logs capture names, emails, card numbers, tokens - masking at the logging layer (PAN `****1234`, phone `+7 9XX XXX XX XX`, email partially starred) is a default, not an option; the masking rules get stricter when card data is in play ([[What is PCI DSS]]).
- **Minimization**: SP 800-122's core recommendation ladder - collect only what the purpose needs, limit access to it, encrypt at rest and in transit ([[What is AES]]), and set retention limits so old data stops being a liability.
- **Access discipline**: PII access is the textbook case for least privilege and object-level authorization - an IDOR in a profile service is a PII breach by definition ([[What is the principle of least privilege]], [[How would you explain IDOR]]).
- **Adjacent law**: GDPR's "personal data" is broader than PII (pseudonymous data counts, an IP can be personal), so a PII-handling program is the floor, not the ceiling, for EU-facing systems.

> [!warning] "We anonymized the dataset - we removed the names"
> Removing direct identifiers rarely de-identifies: the ZIP-plus-birthdate-plus-gender join re-identifies most people in a dataset, device fingerprints re-attach behavior to identities, and "temporary" unmasked debug tables become permanent. Genuine anonymization is hard statistical work; everything else is pseudonymization that still inherits full protection obligations - and unmasked copies in analytics environments are the classic finding ([[What is the OWASP Top 10]]'s Cryptographic Failures class usually names where the controls were missing).

> [!tip] Interview answer
> PII is NIST SP 800-122's category: information that distinguishes or traces a person - direct identifiers like name, SSN, biometrics, and crucially any linked-or-linkable data such as medical, financial, employment. Engineering practice: minimize collection, mask logs and displays, encrypt at rest and in transit, gate access with least privilege and real authorization checks - remembering that linkable combinations, not just names, make data personal.
