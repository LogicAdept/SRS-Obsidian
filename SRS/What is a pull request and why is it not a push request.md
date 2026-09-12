<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What is a pull request and why is it not a push request

> [!abstract] Short answer
> A **pull request (PR)** is a *platform-level proposal to merge one branch into another*: "I pushed commits to my branch — please pull them into main after review." It bundles the diff, review discussion, approvals, CI status, and the final merge action. It is called **pull** because the direction of intent is *toward the maintainer* — you ask them to pull your work — not because you pull anything. GitLab calls the same object a **merge request**, which is honestly the better name. Git itself has no PR concept — it is hosting-layer collaboration.

## What a PR actually consists of

Source branch → target branch (usually a feature branch → protected `main`), and around that pair the platform assembles the workflow: the **diff** of `target…source` (computed live as you push more commits), **status checks** — CI builds, tests, linters that must pass ([[What is CI]]), **review** — required approvals, line comments, requested changes, and the **merge decision** — merge commit, squash, or rebase-merge per repository policy ([[What kinds of Git branch merges exist]] maps the three). Because the target is usually *protected* ([[Why should you not rewrite history of shared branches]]), the PR is not bureaucracy — it is the only door into main, and CI gates it.

## Why "pull" — the classic interview question

From the maintainer's chair, your work *arrives by pull*: early open-source flow was literally "run `git pull <contributor's-url> <branch>`" — Linus pulled patches this way. The formalized request "please pull from my fork" inherited the word: *you* push to your branch; *they* pull from it. GitHub froze the name as "pull request" even though the button performs a merge; GitLab renamed it *merge request*, describing what actually happens. The deeper point the question probes: **push and pull are directions of data between repositories** ([[How do you download changes from a remote Git repository]]), while a PR is a *conversation about a proposed pull* — direction of *intent*, not of bytes.

> [!warning] A PR is a moving target — and mergeability is computed, not stored
> Pushing new commits to the source branch changes the diff under review; reviews of earlier commits can become stale — platforms mark "outdated" conversations, and re-requesting review after a rebase ([[How does Git rebase differ from merge]]) is etiquette, not paranoia. The "mergeable" badge is *recomputed* against the current target: main moving under your PR can introduce conflicts ([[What is a merge conflict and how do you resolve it]]) that only exist at the platform level — locally your branch was clean. And squash-merging rewrites the branch into one commit with a *new id*: any tooling that pinned the branch's shas ([[What is git blame and how is it used]]'s trail) follows the PR link, not the hashes.

```d2
direction: right
feat: "feature branch\nin your clone" {
  width: 280
  height: 100
  style.fill: "#e3f2fd"
}
push: "git push" {
  width: 180
  height: 80
}
pr: "Pull request\ndiff + review + CI checks" {
  width: 360
  height: 120
  style.fill: "#fff3e0"
}
main: "protected main" {
  width: 260
  height: 100
  style.fill: "#e8f5e9"
}
feat -> push
push -> pr: "open PR"
pr -> main: "merge after green + approvals"
```

**Fig. 1.** The PR is the gate between your branch and the protected line: push freely, enter deliberately.

> [!tip] Interview answer
> **A pull request is the platform's proposal-to-merge: source branch into target, wrapped with the live diff, required CI checks, reviews and the merge action. The name is directional etiquette — you push your branch, but the maintainer is the one who pulls, so the request asks them to pull your work; GitLab's merge request name is more literal. Git itself only knows branches and repositories — the PR is the hosting layer, and it is the enforcement point for protected branches: no PR, no path to main.**

