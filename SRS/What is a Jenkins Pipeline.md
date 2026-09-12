<!--
reps: 0
priority: 0
-->
#DevOps/CICD/Jenkins #SRS

# What is a Jenkins Pipeline

> [!abstract] Short answer
> **Jenkins Pipeline** is a suite of plugins and a DSL that models a delivery pipeline **as code**: the whole build-test-deliver process is written in a text file — the `Jenkinsfile` — committed to the project's repository, so the pipeline is versioned, reviewed, and audited like any other code. It replaces chaining Freestyle jobs by making the staged flow a first-class Jenkins object.

The vocabulary is four concepts. A **Pipeline** is the user-defined model of the whole process. A **node** is a machine in the Jenkins environment able to execute work — and the `node {}` block is the container for Scripted syntax. A **stage** is a conceptually distinct slice of the flow (`Build`, `Test`, `Deploy`) that plugins visualize as progress. A **step** is a single task: `sh 'make'` runs a shell command, `junit 'reports/**/*.xml'` aggregates test reports — steps are the atoms shared by both syntaxes. Committing the Jenkinsfile buys four documented benefits: pipelines are automatically created for all branches and pull requests, pipeline changes go through code review, every change leaves an audit trail, and the file is the single source of truth shared by the whole team.

```java
// Conceptual Declarative Jenkinsfile (official example shape)
pipeline {
    agent any                      // allocate an executor + workspace
    stages {
        stage('Build') {
            steps { sh 'make' }
        }
        stage('Test') {
            steps {
                sh 'make check'
                junit 'reports/**/*.xml'
            }
        }
        stage('Deploy') {
            steps { sh 'make publish' }
        }
    }
}
```

**Listing 1.** The canonical Declarative skeleton: `agent` allocates an executor and workspace, stages group steps, `junit` collects reports.

## Why pipeline-as-code changed Jenkins

Beyond reviewability, the Pipeline plugin made runs **durable** — a pipeline survives planned and unplanned restarts of the Jenkins controller — and **pausable**: an `input` step can stop the flow and wait for human approval, which is how the production gate of [[What is a CI CD pipeline]] is expressed natively. Pipelines are **versatile** (fork/join, loops, parallel stages) and **extensible** through Shared Libraries, which let teams factor repeated stage logic into reusable functions. This is the difference from the Freestyle era, where a multi-stage flow was an outdoor chain of jobs glued by triggers, with no single file describing it.

> [!warning] Defining the pipeline in the UI defeats the point
> Jenkins allows entering the same pipeline definition through the web UI, and teams that do so lose code review, the audit trail, and the single source of truth — the pipeline then rots in one admin's head. The second trap is treating a Pipeline as a shell-script container: everything nested in one `sh` step hides stage semantics, breaks visualization, and skips per-stage error handling. The name also invites confusion — "Jenkins Pipeline" (the plugin suite and DSL) is not the same subject as a generic CI/CD pipeline, which is the tool-neutral concept in [[What is a CI CD pipeline]].

> [!tip] Interview answer
> **A Jenkins Pipeline is Jenkins' pipeline-as-code: a Jenkinsfile in the repository defines stages — Build, Test, Deploy — as pipeline, agent, stage, and step blocks, and every branch or PR gets the build automatically. It survives controller restarts, can pause for approvals, and is versioned, reviewed, and audited like application code. Steps like sh and junit are the atoms; Shared Libraries factor out repetition. It is the replacement for chaining Freestyle jobs.**
