<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# How does Panache remove getters and setters

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: Panache generates public accessors for public fields at build time via bytecode transformation (Gizmo) so Hibernate still uses getters/setters internally; field access is allowed directly.
The trick: you write entity fields, the accessor bytecode appears in the compiled class — build-time code generation, not runtime proxying.
