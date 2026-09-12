<!--
reps: 0
priority: 0
-->
#Networking/DNS #SRS
# What is DNS and how does DNS resolution work

> [!abstract] Short answer
> DNS (RFC 1034/1035) is the hierarchical, distributed database that maps names (example.com) to records (mostly IP addresses). Resolution walks the hierarchy: a stub resolver asks a recursive resolver, which — if its cache misses — queries a root server (".", which delegates), then the TLD server (.com), then the authoritative server of example.com, and caches each answer for its TTL. Protocol-wise DNS uses UDP port 53 for ordinary queries (TCP for large answers or zone transfers, HTTPS/TLS variants for encrypted transport).

## The resolution walk

1. **Stub resolver** (in your OS) asks its configured **recursive resolver** (your router, ISP's, or 8.8.8.8/1.1.1.1): "A record for example.com?"
2. **Cache check:** the recursive resolver returns cached answers immediately, honoring each record's TTL; NXDOMAIN is cached too.
3. **On miss — iterative delegation:** it asks a **root server**, which does not know the answer but knows who runs `.com` (returns NS records); it asks a **TLD server**, which delegates to example.com's **authoritative servers**; the authoritative server answers with the A record (and its TTL).
4. **Response:** the resolver caches the answer (and the delegation info), returns the record to the stub; the OS hands the IP to the application.

```d2
direction: down
stub: "Stub resolver\n(OS / browser)" { width: 220; height: 70; style.fill: "#e8f5e9" }
rec: "Recursive resolver\ncache: TTL-bounded" { width: 240; height: 80; style.fill: "#fff3e0" }
root: "Root servers (.)\ndelegate .com" { width: 230; height: 70; style.fill: "#e3f2fd" }
tld: ".com TLD servers\ndelegate example.com" { width: 240; height: 70; style.fill: "#e3f2fd" }
auth: "Authoritative NS\nexample.com -> 93.184.x.x" { width: 260; height: 80; style.fill: "#fff3e0" }
stub -> rec -> root -> tld -> auth
```

**Fig. 1.** Recursion on the left edge, delegation chain through root → TLD → authoritative — each level only says "ask there".

## Properties worth naming in an interview

- **Hierarchy and decentralization:** zones (portions of the namespace, e.g. example.com) are delegated and administered separately; the root zone anchors trust.
- **Caching + TTL:** every record carries a TTL; resolvers must expire answers — this is how DNS changes propagate and why "it still resolves the old IP" happens (negative caching included).
- **Redundancy:** zones publish multiple NS servers; anycast puts copies of root/TLD/authoritative servers worldwide.
- **Transport:** ordinary queries fit one UDP datagram; truncation (TC flag) makes the stub retry over TCP; DoT/DoH encrypt the leg to the resolver.

> [!warning] "The resolver finds the IP by asking the root for the name" — wrong direction
> Roots only know delegations for TLDs, not individual names; a resolver *walks* referrals. Also: DNS resolves *names*, not URLs — there is no "DNS lookup for a full page address"; only the hostname part goes to DNS. And hosts files, mDNS (.local) and browser caches sit in front of real DNS more often than people admit ([[What does a Layer 2 broadcast look like in a packet capture]] covers the LAN-side mDNS/ARP chatter).

Related: [[What are common DNS record types]] for the payload vocabulary, [[What happens when you type a URL into a browser and press Enter]] for where resolution sits in the full chain, and [[How do containers find each other by name on a Docker network]] for the docker-embedded resolver.

> [!tip] Interview answer
> DNS is a hierarchical distributed database for name-to-record mapping. Resolution: stub → recursive resolver (cache first, TTL-bounded), then iterative referral walk — root nameserver says who runs .com, TLD says who is authoritative for the domain, authoritative NS returns the record; every hop caches by TTL. Transport is UDP 53 with TCP fallback on truncation. The two follow-ups I expect: caching/NXDOMAIN behavior and DoH/DoT privacy.
