<!--
reps: 0
priority: 0
-->
#Security/Authorization #SRS

# What is the principle of least privilege

> [!abstract] Short answer
> Least privilege means every subject - user, service, process - gets the **minimum permissions required for its current task, and nothing more**, for only as long as needed. NIST's glossary (SP 800-53 family) phrases it as granting each subject "the most restrictive set of privileges needed" for its role. It is the single control that most reliably shrinks blast radius when anything else fails: a leaked token can only do what the token could do.

## Where it bites in a backend

- **Database accounts**: the app account gets DML on its own schema - not DDL, not superuser, not read on other schemas. A SQLi hole in the app then hits a wall instead of the whole server ([[How would you explain SQL injection attacks and defenses]]).
- **Containers and OS**: run as non-root, read-only filesystems, dropped capabilities; a compromised container should not be root on the host ([[How do you run a Docker container as a non-root user]]).
- **Cloud IAM**: per-service roles with explicit actions and resources - `s3:GetObject` on one bucket prefix, not `"Action": "*"` on `"Resource": "*"`.
- **CI/CD**: pipeline jobs get scoped, short-lived tokens per job, not a tenant-wide deploy key ([[How do you manage secrets in CI CD pipelines]]).
- **Human access**: standing admin rights replaced by just-in-time elevation with approval and expiry (sudo, PIM).

```text
GRANT SELECT, INSERT, UPDATE ON app.orders TO app_user;
-- no DELETE, no DDL, no other schemas, nopg_* extensions
```

**Listing 1.** A least-privilege DB grant: exactly the verbs the application performs. Revocation-by-default is the point - privileges exist because someone listed them, not because nothing forbade them.

## The economics

Least privilege converts a single catastrophic failure into a bounded one: with wildcard IAM the leaked key is the incident; with scoped roles the leaked key is one query returning 403s. The costs are real - more roles to design, occasional "permission denied" in production - which is why privilege *accumulates* by default in older systems: every incident adds an "temporary" grant that nobody removes.

```d2
direction: right
leak: "Credential leaked" { width: 190; height: 70; style.fill: "#ffebee" }
wide: "Wildcard IAM\n-> full tenant access" { width: 240; height: 80; style.fill: "#ffebee"
narrow: "Scoped role\n-> one action, one resource" { width: 240; height: 80; style.fill: "#e8f5e9"
leak -> wide
leak -> narrow
```

**Fig. 1.** The same leak, two blast radii. Least privilege is what the attacker is allowed to do *after* the first line fails.

> [!warning] "We gave the service admin because debugging is easier"
> That is privilege persistence, not privilege. The debugging need should be met by time-bound elevation with audit, not standing rights - a standing admin key in CI is the classic initial-access vector ([[What is zero trust architecture]]).

> [!tip] Interview answer
> Least privilege is deny-by-default: each user, service, and pipeline gets the narrowest set of actions on the narrowest set of resources, ideally time-bound. It shows up everywhere - DB grants, non-root containers, scoped IAM, JIT admin access - and its value is blast radius: whatever fails first, the attacker lands at the edge of a small permission set, not at admin.
