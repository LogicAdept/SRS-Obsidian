<!--
reps: 0
priority: 0
-->
#Security/AppSec #SRS

# How would you explain IDOR

> [!abstract] Short answer
> Insecure Direct Object Reference is accessing another user's data by manipulating an object identifier in a request - `/orders/1023` becomes `/orders/1024` - when the server never checks **that this user may see this object**. The missing control is object-level authorization; OWASP's API listing puts it at the top of API risks, and it is the everyday face of Broken Access Control in the Top 10.

## The anatomy

```d2
direction: right
u: "User A\nauthenticated" { width: 180; height: 70; style.fill: "#e3f2fd"
req: "GET /api/orders/1024\nid changed by hand" { width: 250; height: 80; style.fill: "#ffebee"
chk: "Server: is 1024 owned by User A?" { width: 300; height: 80; style.fill: "#fff3e0"
no: "No check - record returned\n(IDOR)" { width: 260; height: 80; style.fill: "#ffebee"
yes: "Check present - 403" { width: 200; height: 70; style.fill: "#e8f5e9"
u -> req -> chk
chk -> no
chk -> yes
```

**Fig. 1.** The whole bug is the missing branch: authentication confirms *who* is asking, and nothing confirms *that this principal owns this object* ([[What is the difference between authentication and authorization]]).

What makes it pervasive:

- Identifiers are visible by design: sequential IDs in URLs, JSON body keys, GraphQL object IDs, file names.
- Frameworks make the fetch one line and the check nothing: `orderRepository.findById(id)` has no notion of "yours".
- Tests rarely exercise cross-user access - User B reading User A's object is not in the happy-path suite.

```java
// vulnerable: object fetched, identity ignored
Order o = orders.findById(id);
// fixed: the query itself scopes by principal
Order o = orders.findByIdAndUserId(id, currentUser.getId())
        .orElseThrow(NotFoundException::new);
```

**Listing 1.** The fix is server-side scoping of every object read/write by the authenticated principal - a policy, not a datatype change ([[What is the principle of least privilege]]).

## Prevention that actually holds

- **Object-level authorization on every access path** - REST handlers, GraphQL resolvers, file downloads, export jobs; centralize it (policy engine, repository-level scoping) so a forgotten endpoint is the exception ([[What is hasPermission in Spring Security method expressions]]).
- **Random identifiers are hardening, not the fix**: UUIDs slow enumeration but the direct reference is still directly accessible if the check is missing - predictability of the ID was never the vulnerability.
- **Deny consistently**: same error (usually 404) whether the object is absent or foreign, so probing does not distinguish "not exists" from "not yours".
- **Automated cross-user tests**: a suite that logs in as two users and asserts isolation per resource type.

> [!warning] "We use GUIDs, so IDOR is impossible"
> GUIDs make guessing hard, not access denied - a leaked URL, shared email link, or browser history hands over the reference, and the missing check is still missing. IDOR is an authorization defect; the identifier's entropy is a separate topic ([[What is the OWASP Top 10]] groups it under Broken Access Control for exactly this reason).

> [!tip] Interview answer
> IDOR is the missing object-level authorization check: change the ID in the request, get someone else's record. The fix is scoping every read and write by the authenticated principal - in queries, resolvers, and downloads - with uniform 404s and cross-user tests. Random IDs are obfuscation; the check is the control.
