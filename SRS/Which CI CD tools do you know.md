<!--
reps: 0
priority: 0
-->
#DevOps/CICD #SRS

# Which CI CD tools do you know

> [!abstract] Short answer
> The landscape splits into three generations: **classic standalone servers** — Jenkins (plugins, self-hosted, still the enterprise default), TeamCity (JetBrains, developer-friendly), Bamboo, and the legacy Hudson; **built-in platform CI** — GitHub Actions, GitLab CI/CD, Bitbucket Pipelines — pipelines described in YAML next to the code, runners provided or self-hosted; and **pipeline-as-code specialists** — Jenkins' declarative pipelines, Tekton/Argo/Flux in the Kubernetes-native world, plus orchestrators like Ansible/Terraform that CD stages shell out to. What matters at interview: the *pipeline-as-code* shift (committed, reviewed, versioned pipelines) and knowing one tool per generation concretely.

## One tool per generation, concretely

**Jenkins** — self-hosted Java server; power is the plugin ecosystem (thousands), cost is the same ecosystem (upgrade drift, security surface). Modern Jenkins projects define pipelines in a committed `Jenkinsfile` (declarative stages), run steps on agents, and integrate [[What are Git hooks]]-equivalent triggers via webhooks. Legacy note interviewers like: Hudson was Jenkins' pre-Oracle name.

**GitHub Actions** — YAML workflows in `.github/workflows/`, triggered by repo events (push, PR, schedule, tags); jobs run on hosted or self-hosted runners; the marketplace supplies reusable actions — CI/CD for the platform your repo already lives on ([[What is the difference between Git and GitHub]]), with the PR status checks that gate merges ([[What is a pull request and why is it not a push request]]).

**GitLab CI/CD** — the same idea native to GitLab: `.gitlab-ci.yml` describes stages; runners execute; review apps and environments connect the pipeline to deployments (GitLab Flow's environment branches — [[What Git branching strategies do you know]] — map onto it directly).

**TeamCity** — JetBrains' server with build chains and strong IDE-integration; common where JetBrains tooling is standard. **Bamboo** — Atlassian's, common in Jira/Bitbucket shops. **Tekton/Argo/Flux** — Kubernetes-native CI/CD, where pipelines and GitOps delivery are CRs on the cluster ([[What is CI]]'s CD extension mechanized).

```d2
direction: right
repo: "Git repository\n(committed pipeline definition)" {
  width: 330
  height: 110
  style.fill: "#e3f2fd"
}
trig: "Trigger\npush / PR / tag / schedule" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
run: "Runner / agent\nbuild -> test -> package" {
  width: 320
  height: 110
  style.fill: "#e8f5e9"
}
out: "Status + artifact\n(gate to deploy)" {
  width: 290
  height: 100
  style.fill: "#f3e5f5"
}
repo -> trig
trig -> run
run -> out
```

**Fig. 1.** Every modern CI tool is this loop with different syntax: the pipeline definition lives in the repo, the runner executes it, status/artifacts flow back.

## Choosing — the interview-worthy tradeoffs

**Self-hosted (Jenkins, TeamCity, self-hosted runners)**: full control, private networks, unlimited minutes — at the price of operating the controllers/agents. **SaaS built-in (Actions, GitLab.com)**: zero ops, native repo integration, generous-enough free tiers — at the price of per-minute costs at scale and platform coupling. **Pipeline-as-code everywhere**: committed YAML/Jenkinsfile means pipelines get review, history and rollback like any code — the non-negotiable maturity marker; clicking pipelines together in a UI is the legacy smell. For Java shops the common answer: Jenkins (inherited estate) *or* GitLab/Actions (greenfield), Maven/Gradle as build core ([[Which build tools for Java do you know]]), artifacts to Nexus/Artifactory.

> [!warning] Tools do not make continuous integration — and secrets in CI configs are the standing risk
> A Jenkins server running nightly builds is build automation, not CI ([[What is CI]] — the integration cadence is the practice). The eternal foot-gun: credentials needed by pipelines end up committed in the YAML or Jenkinsfile — platform secret managers (vaults, masked variables, OIDC-to-cloud) exist for exactly this; a leaked CI credential leaks every environment it deploys to. Runner hygiene is the sibling risk: self-hosted runners execute PR-triggered code — isolate or gate them, or a hostile PR executes on your network.

> [!tip] Interview answer
> **Three generations: classic self-hosted servers — Jenkins with its plugin estate and committed Jenkinsfiles, TeamCity, Bamboo, and Hudson as Jenkins' ancestor; platform-native CI — GitHub Actions and GitLab CI/CD with YAML pipelines next to the code and hosted runners; and Kubernetes-native stacks like Tekton and Argo for GitOps delivery. The maturity markers I'd look for: pipeline definitions committed and reviewed, merge gates wired to status checks, secrets in vaults rather than YAML — and I'd note Jenkins' cost is precisely its plugin flexibility.**

