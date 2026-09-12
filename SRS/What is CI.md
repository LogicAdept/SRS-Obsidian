<!--
reps: 0
priority: 0
-->
#DevOps/CICD #SRS

# What is CI

> [!abstract] Short answer
> **Continuous Integration (CI)** is the practice of integrating every developer's work into the shared mainline *frequently* — at least daily — with each integration automatically **built and tested** so integration errors surface within hours, not weeks. The enabler is automation on the hosting side: every push or pull request triggers a pipeline (compile, unit tests, linters, security scans) whose green/red status gates the merge. CI is a *practice*; Jenkins, GitLab CI, GitHub Actions and TeamCity are tools that implement it — and the term is routinely misused for the tools.

## The practice, not the server

The textbook contract: frequent integration, an automated build with a self-testing structure, fast feedback, and "don't comment out the failing test". Under [[What Git branching strategies do you know]], this is exactly why trunk-based and GitHub Flow models exist — short-lived branches are *cheap to integrate* only when the integration is verified automatically each time. For a Java backend the canonical pipeline stages are: compile → unit tests → static analysis → integration tests (often against containers) → package artifact → publish report/manifest. The VCS is the trigger and the record: every run is bound to a commit id ([[What does a commit object contain]]), which is what makes "green on main" a meaningful, auditable claim.

```d2
direction: right
push: "git push / PR" {
  width: 230
  height: 90
  style.fill: "#e3f2fd"
}
pipe: "Pipeline\nbuild -> test -> analyze" {
  width: 340
  height: 110
  style.fill: "#fff3e0"
}
gate: "Status on PR\nmerge allowed only when green" {
  width: 340
  height: 110
  style.fill: "#e8f5e9"
}
main: "main\nalways releasable" {
  width: 260
  height: 90
  style.fill: "#f3e5f5"
}
push -> pipe
pipe -> gate
gate -> main
```

**Fig. 1.** CI closes the loop between version control and quality: the merge gate is the practice made mechanical.

## CI versus the words that come after it

**Continuous Delivery** extends CI to "every green build is *packaged and ready* to deploy to production with one manual click"; **Continuous Deployment** removes the click — every green build ships. So CI answers "does the integrated code work", CD answers "is it releasable/shipped". Related mechanics: a **pipeline** is the configured sequence of stages ([[What is a CI CD pipeline]] covers the term); **trunk-based flow** ([[How does trunk based development differ from long lived feature branches]]) is what makes CI *meaningful*, because integration actually happens continuously; **protected branches** ([[Why should you not rewrite history of shared branches]]) are how the "green before merge" rule is enforced rather than hoped for.

> [!warning] CI without integration is just build automation — and broken main defeats the whole point
> A pipeline that runs only on long-lived feature branches validates code nobody can merge confidently; the "continuous" in CI refers to *integrating into the mainline*, which is a team behavior, not a server feature. The classic anti-patterns: red main (everyone proceeds locally, trust is gone), slow pipelines that push teams to merge unverified (ten-minute budget per stage is the pragmatic ceiling), flaky tests that train people to ignore red, and commenting out tests instead of fixing them — the shortest path to losing CI's value entirely. Note also what CI is *not*: it does not replace local pre-commit feedback ([[What are Git hooks]]) and does not decide deployment policy — that is CD's territory.

> [!tip] Interview answer
> **CI is the practice of integrating work into the shared mainline at least daily, with every push automatically built and tested so integration errors surface in hours. It is enforced as a merge gate on pull requests and bound to commit ids for auditability; trunk-based short branches are what make it real rather than nominal. Continuous delivery extends it to always-releasable artifacts and continuous deployment to automatic shipping — CI says the integrated code works, CD decides what ships. Tools implement it; the practice — green main, fast pipelines, no skipped tests — is the actual content.**

