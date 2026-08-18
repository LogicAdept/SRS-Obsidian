<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A persisted query registers query text on the server and gives it a hash. Clients send the hash plus variables, not the full string. Automatic persisted queries: send the hash first; send full text only on a miss.

Dump wins: smaller payloads; GET with hash can be CDN-cached; allowlist so the server refuses unknown hashes (blocks arbitrary expensive queries). Pairs with security on public APIs.

> [!warning] Unverified traps from the dump
> - Dump claim: APQ without an allowlist still lets unknown queries in after the first full-text miss.
