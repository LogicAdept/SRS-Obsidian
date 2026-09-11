<!--
reps: 0
priority: 0
-->
#Databases #DevOps/VCS/Git #SRS

# What merge strategies are important in database development

> [!abstract] Short answer
> **Treat schema changes as versioned, append-only code: migrations are ordered by version, never rewritten after being applied, and merges are coordinated so two branches cannot produce conflicting or re-ordered changes against the same database.** The dangerous merges are not in code — they are two branches both editing the schema history.

## The rules that make database merges survivable

**Append-only history.** A migration already applied to shared environments gets its checksum frozen (Flyway records a checksum in its schema history table; Liquibase identifies changesets by author:id plus changelog path). Editing an applied file makes the next run fail verification on every environment that has it. The correct fix for a mistake is a **new forward migration** that alters the schema again — or, for released-but-never-applied work, a coordinated edit before anyone runs it.

**Ordering discipline.** Two branches each adding `V7__...` collide: on merge, one database ran V7 from branch A while branch B's V7 never ran anywhere. Strategies: strictly sequential version numbers with rebase-before-merge (simple, contention-prone), timestamp-based versions like `V2026.09.11.101__` (contention-free, out-of-order inserts detected by Flyway), or one-changelog-per-feature with include-graphs (Liquibase's answer to minimizing conflicts between teams). Whichever you pick, the merge gate is the same: CI runs migrations against a scratch database from empty and from the previous release, so an ordering conflict fails the build instead of production.

**Semantic conflicts.** Both branches may merge textually clean while contradicting each other — branch A renames `email` to `work_email`, branch B adds an index on `email`. Git sees no clash; the scratch-database run exposes it. Expand-contract conventions (add-new, migrate, drop-old in separate releases) shrink the window where such conflicts can exist at all.

```d2
direction: right
a: "Branch A\nV7 add status" {
  width: 190
  height: 80
  style.fill: "#e3f2fd"
}
b: "Branch B\nV7 add tax_id  (same number!)" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}
ci: "CI: apply all migrations\nto a scratch database" {
  width: 290
  height: 90
  style.fill: "#fff3e0"
}
ok: "Pass: linear history\nor timestamp order" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
a -> ci
b -> ci
ci -> ok
```

**Fig. 1.** The merge gate replays the combined migration set on a clean database; duplicate or out-of-order versions fail there, before any shared environment sees them.

> [!warning] Code merges clean while the schema still conflicts
> Git compares text, and migration files from two branches rarely touch the same lines — so `git merge` reports success while the history is broken. The only trustworthy check is applying the merged set to an empty scratch database in CI. Squashing "to tidy up" migration files that already shipped is the same trap in another form: environments that already ran them will fail verification.

Keep the release mechanics in [[How do you do blue-green deployments that include a database]] and the tool layer in [[What is the difference between Liquibase and Flyway]].

> [!tip] Interview answer
> I treat migrations as append-only artifacts with an ordering rule: version numbers sequential or timestamp-based, applied files immutable, fixes as new forward migrations. Merges are validated by CI applying the full set to a scratch database — that catches duplicate versions and semantic conflicts that text merges cannot see — and destructive changes ship late, in the contract phase of expand-contract.
