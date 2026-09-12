<!--
reps: 0
priority: 0
-->
#Networking/DNS #SRS
# What are common DNS record types

> [!abstract] Short answer
> The record types you meet daily: A (IPv4 address), AAAA (IPv6), CNAME (alias to another name), MX (mail server + priority), NS (delegation to authoritative servers), TXT (arbitrary text — SPF, DKIM, verification), SOA (zone metadata: serial, refresh, retry), PTR (reverse lookup, IP → name), SRV (service location with port), CAA (who may issue certificates for the zone). The registry of all types is maintained by IANA.

## The working set

| Type | Answers "…" | Example |
|---|---|---|
| A | what IPv4 for this name? | example.com → 93.184.216.34 |
| AAAA | what IPv6? | example.com → 2606:2800:... |
| CNAME | which other name owns the records? | www.example.com → example.com |
| MX | which host takes mail, in what priority? | 10 mail.example.com |
| NS | which servers are authoritative? | ns1.example.com |
| TXT | free text: SPF/DKIM/ownership proofs | "v=spf1 include:..." |
| SOA | zone's source of authority: serial, refresh, retry, expiry, minimum | ns1 admin... 2024010101 7200 3600 ... |
| PTR | reverse DNS: what name belongs to this IP? | 34.216.184.93.in-addr.arpa → example.com |
| SRV | where does a service run? (_service._proto) | _sip._tcp → host, port, weight, priority |
| CAA | which CAs may issue certs for this domain? | 0 issue "letsencrypt.org" |

```d2
direction: right
q: "Lookup www.example.com A" { width: 240; height: 70; style.fill: "#e3f2fd" }
cn: "www.example.com CNAME\n-> example.com" { width: 280; height: 80; style.fill: "#fff3e0" }
a: "example.com A\n-> 93.184.216.34" { width: 260; height: 70; style.fill: "#e8f5e9" }
q -> cn -> a
```

**Fig. 1.** A CNAME chain costs an extra lookup: the resolver follows aliases until it lands on address records.

## Rules and gotchas

- **CNAME cannot coexist with other records at the same owner name** (RFC 1034's restriction) and is illegal at a zone apex — that is why registrars offer ALIAS/ANAME vendor extensions and why apexes need A/AAAA directly. When asked "why can't I CNAME the root?", that is the answer.
- **TTL is per record** and governs caching ([[What is DNS and how does DNS resolution work]]) — low TTL before a migration, high TTL for stability.
- **PTR requires the .in-addr.arpa zone** (IPv6: .ip6.arpa) and is controlled by whoever owns the *address* block — usually the hosting provider, not you.
- **MX has priorities** (lower wins first); **SRV** generalizes the idea for other services.

> [!warning] "A record stores the domain name of the server" — the classic flip
> A maps name → IPv4 address; the *name → name* redirection is CNAME; the *IP → name* direction is PTR. Mixing those three is the most common interview slip. Another trap: "TXT is only for human notes" — it is the workhorse of SPF, DKIM and site-verification tokens (IANA keeps the full registry, including oddballs like SSHFP and TLSA).

Context: [[What is DNS and how does DNS resolution work]] for the machinery that serves these records, [[What is the difference between HTTP and HTTPS]] for where CAA/TLSA connect to certificate practice.

> [!tip] Interview answer
> I group them: addresses — A and AAAA; aliases — CNAME (not at the apex, no coexistence with other records); mail — MX with priority; delegation and zone control — NS and SOA; metadata — TXT for SPF/DKIM/verification, CAA for certificate policy; reverse — PTR under in-addr.arpa; services — SRV. The detail that shows depth: apex CNAME restrictions and per-record TTL semantics.
