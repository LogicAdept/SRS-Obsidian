<!--
reps: 0
priority: 0
-->
#DevOps/Deployment/Strategies/BlueGreen #SRS

# What is blue-green deployment

> [!abstract] Short answer
> **Blue-green deployment** keeps two production environments as identical as possible; one is live (say blue), while the new release is deployed and final-tested in the other (green). Going live is a single router switch from blue to green, and **rollback is the same switch in reverse** — the old environment stays intact until the new one has proven itself.

The technique exists to make the cut-over itself boring: instead of upgrading the live environment in place (with its downtime and half-migrated state), you prepare the release in an idle twin and flip traffic atomically. The environments can be separate hardware, separate virtual machines, or one operating environment partitioned into zones with separate addresses — the requirement is "different but as identical as possible". After the switch, the roles cycle: the previously live environment becomes first the rollback target, then the staging twin for the *next* release. A documented bonus: the mechanism is the same as a hot-standby, so every release rehearses the disaster-recovery switch ([[How does Kubernetes achieve high availability]] builds the same redundancy idea into the platform itself).

```d2
direction: right
router: "Router / LB\ntraffic switch" {
  width: 260
  height: 100
  style.fill: "#e3f2fd"
}
blue: "Blue: live v1.4\nserving 100%" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
green: "Green: v1.5\nfinal testing" {
  width: 280
  height: 100
  style.fill: "#fff3e0"
}
db: "Shared database\n(expand-contract schema)" {
  width: 320
  height: 100
  style.fill: "#ffebee"
}
router -> blue
router -> green: "flip"
blue -> db
green -> db
```

**Fig. 1.** Both environments serve the same database, which is why schema changes must be decoupled from the application switch.

## The database is the hard part

Application servers flip atomically; schemas do not. If green ships a column rename while blue still writes the old shape, one side breaks the moment the other deploys. The established discipline — covered end-to-end in [[How do you do blue-green deployments that include a database]] — separates schema deployment from application upgrade: first migrate the schema to a shape that supports *both* versions (expand), deploy and verify with a rollback point, ship the application, and only later remove the old-shape support (contract). In-flight state is the second wrinkle: transactions running during the switch can straddle both environments, so teams either feed transactions to both sides during the window or briefly run read-only before cut-over.

> [!warning] Blue-green is not free
> The cost side is real: double the production infrastructure for the idle twin, and a switch that is atomic for *routing* but not for *state* — sticky sessions, caches, and long-lived connections carry memory of the blue world into the green one. The worst failure is the incompatible-migration trap: a destructive schema change (drop column, tighten a constraint) destroys the rollback path, because the old application cannot run on the new schema — the "switch back" is then a restore, not a flip. And compared with [[What is a canary release]], blue-green is all-or-nothing: it cannot expose 5% of users first; it bets the whole fleet on final testing done in advance.

> [!tip] Interview answer
> **Blue-green keeps two identical production environments, deploys and tests the new release in the idle one, and goes live by a single router switch; rollback is the same switch back, so recovery is measured in seconds. The hard parts are state: database schemas must support both versions through expand-and-contract migrations, and in-flight transactions need a window strategy. It costs double infrastructure and is all-or-nothing traffic-wise, unlike a canary's gradual exposure.**
