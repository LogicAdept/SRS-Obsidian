<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A cross-cutting concern is behavior needed in many places (logging, security, transactions, timing) that does not belong in one domain class.

AOP is one way to implement it: write the concern once as an aspect and apply it via pointcuts instead of copying it into every method.

OOP, AOP, and Spring dumps call complementary: Spring builds dynamic proxies and binds configured advice to those concerns.

> [!warning] Unverified traps from the dump
> - Cross-cutting concern is the problem; AOP is an approach — not synonyms.
