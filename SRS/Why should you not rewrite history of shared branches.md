<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# Why should you not rewrite history of shared branches

> [!abstract] Short answer
> A commit's identity *is* its hash ([[What does a commit object contain]]), so rewriting history means **publishing new ids for the same work**. Every clone built on the old ids then diverges from the remote in a way merges cannot resolve cleanly — teammates see their reviewed commits "disappear" and duplicates reappear, CI reruns on replacements, provenance (releases, image digests, review threads) detaches. Rule: rewrite only history you exclusively own; on shared lines, **append** — `revert`, not `reset`; `force-with-lease`, not bare `--force` when a rewrite is truly necessary.

## What actually breaks

Git has no synchronization concept of "same logical commit, new hash" — after a rewrite, a teammate's `pull` produces a *merge of two unrelated histories*: the pre-rewrite commits and their replacements, both in the graph, double content, conflicts between identical changes. Recovery on their side is manual (`reflog` archaeology, hard resets). Tooling keyed to ids suffers silently: review comments pin to dead commits, `git blame` attributions jump ([[What is git blame and how is it used]]), release tags and image digests built from a rewritten sha describe content that no longer exists on the branch. That is why protected branches exist on hostings: they make rewriting *impossible by policy* ([[What is a tag in Git and how does it differ from a branch]] covers the same discipline for tags).

## When rewriting *is* legitimate

- **Your own feature branch**: rebase onto main, interactive cleanup, amend — even if you pushed it before, as long as nobody pulls it. Re-push with `--force-with-lease`.
- **Before opening a PR**: squash wip commits — the shared line never sees them.
- **Platform-assisted rewrites**: "Squash and merge"/"Rebase and merge" buttons rewrite on the hosting side *at integration time*, and the resulting commits go to main in one atomic step — contributors never reference the intermediates.
- **The sanctioned incident flow**: purging accidentally committed secrets (filter-repo/BFG) — a coordinated rewrite with everyone freezing pushes, followed by credential rotation, because removing the blob does not un-leak it.

## force-with-lease: the guard, verbatim

```text
$ git push --force-with-lease origin topic
To …/shared.git
 ! [rejected]        topic -> topic (stale info)
error: failed to push some refs to '…/shared.git'
$ git push --force origin topic
To …/shared.git
 + b18491b...f526bb2 topic -> topic (forced update)
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): `--force-with-lease` checks that the remote branch still sits where *your last fetch* saw it; a teammate's fresh commit in between rejects the push. Bare `--force` overwrites whatever is there — the clobber that loses someone's work.

> [!warning] force-with-lease is not a licence to rewrite shared branches — and it has a blind spot
> The lease only protects against *unknown* remote changes since your last fetch; if you fetched the teammate's commit into your local tracking ref, the lease matches it happily. Cron-driven `fetch` in the background (some IDE plugins) can silently refresh your lease. And there is no lease at all that protects you from rewriting a branch *nobody currently disagrees with you about* — the rewrite itself is the damage; the lease only narrows the window. Delete-then-recreate, "someone will rebase after", "only for a moment" — all the same incident.

```d2
direction: down
old: "remote: A -> B -> C\n(teammates cloned C)" {
  width: 340
  height: 90
  style.fill: "#e3f2fd"
}
rw: "history rewrite\npublishes B' -> C'" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
team: "teammates hold A -> B -> C\npull => merge of unrelated lines" {
  width: 400
  height: 100
  style.fill: "#ffebee"
}
safe: "append instead:\nrevert commit on top" {
  width: 360
  height: 90
  style.fill: "#e8f5e9"
}
old -> rw: "force push"
rw -> team
old -> safe: "shared branch policy"
```

**Fig. 1.** Rewriting replaces ids under clones that remember the originals; appending (revert) keeps every consumer's assumptions true.

> [!tip] Interview answer
> **Commits are identified by hash, so rewriting shared history publishes different ids for work people already cloned — their pulls produce unrelated-history merges, review threads and release artifacts pin dead commits, and provenance detaches. I rewrite only branches I exclusively own and re-push with force-with-lease, which rejects the push when the remote moved since my last fetch. On anything shared I append instead — revert for undo — and reserve coordinated rewrites like secret purges for explicit team incidents with rotation afterwards.**

