<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A pattern glossary's when-not-to-use list: skip a dedicated invalid channel for simple applications with little error processing, and skip it when the extra channel's complexity outweighs the benefit of separate handling.

Trade-offs in the same list: another channel to operate, extra storage for invalid messages, and a more complicated workflow because invalid traffic is handled off the main path. When-to-use on that page is the opposite: the happy path cannot be disrupted, invalid traffic needs special handling and logging, or invalid transactions need audit and monitoring (financial isolation, e-commerce order review, IoT anomaly inspection).
> [!warning] Unverified traps from the dump
> - Cloud notes on that page also warn that dedicated error channels across a large estate have cost implications.
> - The same glossary still lists Retry and Circuit Breaker as related, which can hide a permanently invalid payload behind retries.
