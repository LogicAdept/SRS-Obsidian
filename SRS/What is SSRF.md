<!--
reps: 0
priority: 0
-->
#Security/AppSec #SRS

# What is SSRF

> [!abstract] Short answer
> Server-Side Request Forgery makes **your server** issue HTTP requests to attacker-chosen targets: a feature that fetches a URL (webhook, URL preview, import) is pointed at internal-only destinations - `localhost` admin panels, peer services, or the cloud metadata address `169.254.169.254` - and the response or its side effects leak. OWASP's prevention cheat sheet grounds the fix in **allow-listing the egress**, network isolation, and not following redirects blindly.

## Why server-side fetches are different

The browser's user is untrusted and unplaced; your server is trusted and *inside* the network. Any feature where user input selects a destination turns that trust around:

- Webhook targets, URL previews/importers, PDF or image renderers, "check this link" validators.
- Internal destinations that matter: admin/actuator endpoints bound to loopback, databases behind the same VPC, and the cloud instance metadata service - which yields credentials on AWS/GCP/Azure.

```d2
direction: right
a: "Attacker\nurl=http://169.254.169.254/..." { width: 270; height: 80; style.fill: "#ffebee"
s: "Public app server\nfetches user-provided URL" { width: 280; height: 80; style.fill: "#fff3e0"
m: "Metadata service\n-> instance credentials" { width: 250; height: 80; style.fill: "#ffebee"
s -> m
a -> s
```

**Fig. 1.** The canonical cloud SSRF: the app server can reach the link-local metadata address; the attacker cannot - unless the app fetches on their behalf.

## Defense layers, per the cheat sheet

- **Allow-list the destination**: scheme, domain, and where possible port - the webhook may call exactly one partner host, and nothing else. Deny-lists lose: `0x7f000001`, decimal and DNS-shortened forms of loopback, subdomain tricks.
- **Disable or constrain redirects**: a check on the first URL is bypassed by a 302 that lands internally; re-validate every hop or do not follow redirects at all.
- **Network isolation**: the fetching service runs in a segment with no route to metadata or admin planes; on clouds, metadata v2-style session tokens require an explicit header, killing trivial SSRF readers ([[What is network segmentation]]).
- **Validate by IP after resolution** - and re-check at connection time, because DNS rebinding swaps the address between the two (TOCTOU).

```java
InetAddress addr = InetAddress.getByName(host);
if (!allowList.contains(host) || addr.isLoopbackAddress() || addr.isLinkLocalAddress()) {
    throw new SecurityException("blocked destination");
}
```

**Listing 1.** Conceptual egress guard: allow-list the host, reject loopback and link-local resolved addresses - and re-resolve at connect to close the rebinding gap.

> [!warning] "We block 127.0.0.1 and 169.254.x.x in a config regex"
> Deny-list by string dies to IP alternatives (0177.0.0.1, 2130706433), DNS names that resolve internally, and redirect hops. SSRF defenses fail as filters and succeed as architecture: allow-list plus network egress rules ([[What is a DMZ in network security]] and [[What is zero trust architecture]] are the same idea pointed inward).

> [!tip] Interview answer
> SSRF turns your server into the attacker's network client: user-chosen URLs are fetched from a trusted position, reaching loopback services, peer services, or the cloud metadata endpoint that hands out credentials. Defenses are allow-listed egress, no unvalidated redirects, rebinding-aware resolution, and network segments where the fetcher simply has no route to the crown jewels.
