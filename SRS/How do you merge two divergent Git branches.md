<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How do you merge two divergent Git branches

> [!abstract] Short answer
> Divergent branches share an ancestor but each has commits the other lacks. Merge is the same operation as always ([[How would you explain the Git merge command]]) — the difference divergent history brings is *which direction you merge from* and the certainty of a three-way result: checkout the branch that should "receive" the work, `git merge <other>`, resolve conflicts ([[What is a merge conflict and how do you resolve it]]), done. For pull-induced divergence, `git pull` merges (or rebases, with `pull --rebase`) origin's state into yours.

## Recognizing divergence, then integrating

```text
$ git log --oneline --graph --all
* a007554 Main: add OrderRepository
| * 8efdc49 Feature: add OrderValidator
|/
* dbe5cb2 Base: OrderService skeleton
$ git merge main                        # standing on feature
Merge made by the 'ort' strategy.
 OrderRepository.java | 1 +
 1 file changed, 1 insertion(+)
$ git log --oneline --graph -3
*   1943e28 Merge main into feature
|\
| * a007554 Main: add OrderRepository
* | 8efdc49 Feature: add OrderValidator
|/
* dbe5cb2 Base: OrderService skeleton
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): both tips moved since the base — `merge` cannot fast-forward, so the `ort` strategy three-way-merges and writes a two-parent merge commit.

Decision checklist for divergent work:

- **Direction**: merging main *into* feature keeps main clean until review time (CI on main never sees an unresolved integration); merging feature into main is the final act of the PR.
- **Update before merging**: `git fetch` first and look at `git log HEAD..origin/main` — merging against a stale target is what manufactures avoidable conflicts ([[How do you download changes from a remote Git repository]] shows the fetch-then-integrate flow).
- **Diverged pull**: `git status -sb` shows `main...origin/main [diverged]`. Either `pull --no-rebase` (a merge commit reconciles) or `pull --rebase` (your local commits replay on origin's tip — ids rewrite, fine while unpushed, [[How does Git rebase differ from merge]]).
- **Same feature, two machines**: the classic "I committed on my laptop and desktop" divergence is solved exactly like any other — fetch, rebase onto the remote tip, force-push *your own* branch with `--force-with-lease` ([[Why should you not rewrite history of shared branches]]).

> [!warning] Divergence that is *invisible* is the dangerous kind
> Two branches can both change the *same file* without Git ever conflicting (different regions), and both can pass tests in isolation while their merge is broken — semantically divergent changes (one renames a method, another adds a call site) merge textually clean and fail at compile time. That is why long-running branches should merge main *into themselves regularly* rather than saving integration for the end — the trunk-based argument in [[How does trunk based development differ from long lived feature branches]]. Note that repeated back-and-forth merges also mean the *next* divergence may fast-forward where you expected a conflict — reading `merge --ff-only` failures is part of the skill.

```d2
direction: down
base: "common ancestor dbe5cb2" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
a: "main: OrderRepository" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
b: "feature: OrderValidator" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
m: "merge commit on feature\n(parents: 8efdc49, a007554)" {
  width: 380
  height: 90
  style.fill: "#f3e5f5"
}
base -> a
base -> b
a -> m: "second parent"
b -> m: "first parent"
```

**Fig. 1.** Divergence means two tips and one base; the merge commit's two parents record exactly those two tips, and the base is the diff anchor.

> [!tip] Interview answer
> **Divergent branches each have commits since the common ancestor, so a merge cannot fast-forward: I fetch to see the real state, stand on the branch that should receive the work, merge the other, and resolve the three-way result — possibly nothing conflicts textually, so I still build and test because semantic clashes survive clean merges. For my own pull-induced divergence I prefer pull --rebase while commits are unpushed; for team branches, a regular merge commit keeps everyone's ids intact.**

