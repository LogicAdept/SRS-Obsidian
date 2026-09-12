<!--
reps: 0
priority: 0
-->
#Security/Authentication #SRS

# What is multi-factor authentication

> [!abstract] Short answer
> Multi-factor authentication (MFA) requires the user to present authenticators from **two or more distinct categories** - something you know (password), something you have (device, TOTP app, security key), something you are (biometrics). NIST SP 800-63B grades the resulting assurance as AAL1-AAL3: a password alone is AAL1, password plus software authenticator reaches AAL2, and hardware-backed, phishing-resistant authentication is AAL3.

## The factor categories and why they must differ

The strength comes from **independence**: a stolen password (knowledge) should not be enough, because the second factor lives in a different category. Two items from the same category - password and PIN - are single-factor in NIST's model, however many secrets were typed.

- **Something you know**: passwords, PINs.
- **Something you have**: TOTP software tokens, push approvals, smart cards, FIDO2/WebAuthn keys - possession is proven by a cryptographic or time-based response.
- **Something you are**: fingerprints, face, iris - bound to a device and best treated as a *local* gate to release a stronger factor, not as a remote check by itself.

```d2
direction: right
u: "User" { width: 120; height: 60; style.fill: "#e3f2fd" }
pw: "Factor 1: password\n(something you know)" { width: 250; height: 80; style.fill: "#fff3e0" }
ot: "Factor 2: TOTP / security key\n(something you have)" { width: 280; height: 80; style.fill: "#e8f5e9" }
v: "Verifier\nAAL2 decision" { width: 200; height: 70; style.fill: "#ffebee" }
u -> pw -> v
u -> ot -> v
```

**Fig. 1.** Two independent authenticator categories feed the verifier; either one alone leaves the account at a lower assurance level.

## Assurance levels and their consequences

- **AAL2** - the typical enterprise bar: two factors, with the possessor factor cryptographically verifiable.
- **AAL3** - hardware-protected keys with verifier impersonation resistance: FIDO2/WebAuthn keys bind the challenge to the *origin*, so a phishing site cannot relay it - a property OTP codes can never have.
- **SMS OTP** is the weakest in class: NIST deprecated PSTN delivery - SIM-swap attacks redirect the code, and the channel can be intercepted.

> [!warning] MFA myths that cost real money
> "MFA stops phishing" - **only phishing-resistant methods do**; a real-time relay (evilginx-style proxy) harvests password *and* live OTP. "Push approval is enough" - push bombing / MFA-fatigue attacks wear users down into approving; number-matching mitigates it. And a second password plus PIN is **not** MFA - same category ([[How should you store and handle passwords securely]]).

And the failure path is a product decision: revoked or lost second factors need a recovery flow that does not become a bypass - account recovery is where MFA quietly degrades back into single factor ([[What is the difference between authentication and authorization]]). Identity providers ship the machinery: OTP enrolment, WebAuthn, and policy per client are core features of [[What is Keycloak]], and Spring wires the same factors into the filter chain ([[How do you implement two-factor authentication in Spring Security]]).

> [!tip] Interview answer
> MFA means authenticators from at least two different NIST categories - know, have, are - mapped to assurance levels AAL1-3 in SP 800-63B. Password plus TOTP is AAL2; a FIDO2 key adds origin binding and verifier impersonation resistance, which is what actually beats phishing relays. SMS codes count but are the deprecated bottom of the list.
