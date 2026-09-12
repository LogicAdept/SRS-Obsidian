<!--
reps: 0
priority: 0
-->
#DevOps/Configuration #SRS

# What is infrastructure as code

> [!abstract] Short answer
> **Infrastructure as code (IaC)** manages infrastructure by **declarative, versioned definitions** instead of manual console clicks: you describe the desired state (networks, machines, DNS, databases) in files, and a tool — Terraform, Ansible, CloudFormation — computes and applies the changes needed to reach it, idempotently and repeatedly. The definition files live in version control, get code review, and produce an auditable history of who changed what and when.

The declarative core: a configuration states *what should exist*, not *how to build it*. In Terraform's language, blocks declare resources — `resource "aws_vpc" "main" { cidr_block = var.base_cidr_block }` — with arguments and references between resources forming the dependency graph; block ordering does not encode execution order, the tool derives it. The workflow is **plan then apply**: `plan` compares the declared state against the real world and prints the diff; `apply` converges reality onto it. What makes convergence possible is **state**: Terraform records the binding between each declared resource instance and the actual remote object (its identity in the provider), stored by default in `terraform.tfstate` and normally moved to a remote backend with locking for team use. Before every operation a refresh pulls current reality into state, which is how drift — someone edited the console — becomes visible as a plan diff.

```hcl
# Conceptual Terraform: declarative desired state
provider "aws" {
  region = var.aws_region
}
resource "aws_vpc" "main" {
  cidr_block = var.base_cidr_block
}
resource "aws_subnet" "az" {
  count             = length(var.availability_zones)
  availability_zone = var.availability_zones[count.index]
  vpc_id            = aws_vpc.main.id      # explicit dependency
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 4, count.index + 1)
}
```

**Listing 1.** Resources declare intent; the reference `aws_vpc.main.id` creates the dependency edge, and `count` fans out one subnet per availability zone.

## Why the practice, not the syntax, is the answer

The interview question is really "how does your team know what exists in production". With IaC the honest answer is: the repository is the source of truth, changes go through review and CI ([[Which CI CD tools do you know]] now includes the apply pipeline), environments are reproducible by re-applying the same definitions, and infrastructure hygiene merges with software hygiene — code review, tests, tags. The complementary pattern is **immutable infrastructure**: instead of patching a live server, you rebuild a new image and replace instances, which eliminates configuration drift by construction and pairs naturally with the deployment techniques in [[What is blue-green deployment]].

> [!warning] State is both the power and the blast radius
> The state file maps declarations to real objects — losing it or corrupting it orphans everything Terraform created, and storing it casually (plain VCS, shared drive without locking) invites both data loss and credential exposure, because state can contain secrets. Hand-editing the JSON is forbidden by the docs; the `terraform state` CLI, `import`, and `rm` subcommands are the sanctioned tools. The process trap is drift by habit: emergency console fixes that are never back-ported into the code — the next plan then either reverts the fix or silently grows a divergence. And "IaC" is broader than Terraform: Ansible's push-based YAML playbooks, CloudFormation, and Pulumi solve the same problem from different angles.

> [!tip] Interview answer
> **Infrastructure as code defines infrastructure in declarative, versioned files that a tool applies idempotently: Terraform plans a diff between declared and real state, then converges. State binds each declared resource to the actual object and must live in a locked remote backend — it can hold secrets and everything depends on it. The practice gives review, reproducibility, drift detection, and audit for infrastructure; combined with immutable images it removes manual patching entirely.**
