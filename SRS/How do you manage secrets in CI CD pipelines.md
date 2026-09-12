<!--
reps: 0
priority: 0
-->
#Security/CICD #DevOps/CICD #SRS

# How do you manage secrets in CI CD pipelines

> [!abstract] Short answer
> Pipeline secrets - deploy keys, cloud credentials, signing keys - are the highest-value credentials in the build estate, so the rules are: **never in code or commit history**, stored in the platform's secret store or an external vault, **injected at runtime into the job only**, scoped per repo and environment ([[What is the principle of least privilege]]), rotated, and **masked in logs**. The modern upgrade for cloud access is replacing long-lived keys with **OIDC federation** - the CI job mints a short-lived token and exchanges it for a scoped role.

## The storage and injection model

```d2
direction: right
g: "Source repo\nNO secrets, ever" { width: 220; height: 80; style.fill: "#e8f5e9"
v: "Secret store\nplatform store or Vault" { width: 250; height: 80; style.fill: "#fff3e0"
j: "Job runtime\nsecrets injected as env/files" { width: 260; height: 80; style.fill: "#e3f2fd"
l: "Logs and artifacts\nmasked, never persisted" { width: 250; height: 80; style.fill: "#ffebee"
g -x j
v -> j
j -x l
```

**Fig. 1.** Three rules drawn as arrows: code never carries secrets; the store feeds the job runtime only; runtime output never echoes secrets back.

- **Platform stores first**: CI-native variables (masked and protected) for the common case; an external vault (HashiCorp Vault, cloud secret managers) when you need rotation, audit, dynamic credentials, or cross-platform sharing - fetched by the job at runtime, not baked into images.
- **OIDC instead of static keys**: GitHub Actions/GitLab CI obtain a short-lived identity token and exchange it with the cloud (AWS/GCP/Azure role federation) - no stored cloud key at all, which removes the theft-and-rotation problem for the majority of jobs.
- **Scoping**: per-repository, per-environment secrets; production deploy credentials exist only for the production deployment job - not as a workspace-wide default.
- **History discipline**: anything committed is considered burned - rotate first, then purge; secret-scanning on push catches the next attempt ([[What is an SBOM]]'s provenance mindset applies: know what a build can touch).

```yaml
permissions:
  id-token: write          # OIDC token for federation
  contents: read
steps:
  - uses: aws-actions/configure-aws-credentials
    with:
      role-to-assume: arn:aws:iam::123:role/deploy-prod   # short-lived, scoped
```

**Listing 1.** The federated shape: the job requests an OIDC token and assumes a scoped role; no cloud secret is stored anywhere in CI.

> [!warning] "It is a private repo, so committing the .env file is fine"
> Private repos leak through forks and clones, CI logs, error traces, artifacts and Docker layers, and a future public-ification or incident dump - and every person who ever had read access holds the secret. Also dead on arrival: "encrypted" or base64-ified variables stored in the repo (encoding is not encryption), and secrets echoed into logs that retention policies then happily archive. Runtime containers need their own discipline - [[How do you manage secrets in Docker at runtime]] covers the per-container half of the story.

> [!tip] Interview answer
> Secrets never live in code, history, or logs: platform secret store or vault, injected per job, scoped per repo and environment, masked in output, rotated. The modern move is OIDC federation - the job swaps a short-lived token for a scoped cloud role, so there is no standing cloud key to steal - and anything that ever hit the repo is rotated before it is cleaned.
