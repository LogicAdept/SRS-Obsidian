<!--
reps: 0
priority: 0
-->
#DevOps/CICD/Jenkins #SRS

# What is the difference between Declarative and Scripted Pipeline

> [!abstract] Short answer
> **Declarative Pipeline** is the opinionated, structured syntax: everything lives in a `pipeline { }` block with fixed sections (`agent`, `stages`, `post`) and directives (`when`, `environment`, `options`), validated before the run. **Scripted Pipeline** is raw Groovy on Jenkins' engine: work happens inside `node { }` blocks with imperative control flow. Both exist since Pipeline plugin 2.5, both use the same steps — the difference is structure versus freedom.

Declarative exists to make pipeline code *readable and uniform* — the shared vocabulary that every [[What is a Jenkins Pipeline]] uses across a company: the top level must be a `pipeline {}` block, no semicolons, blocks contain only sections, directives, steps, or assignments, and the structure is checked at start — a syntax error fails the run before any step executes. Its `post` section declares cleanup by condition (`always`, `failure`, `success`, `fixed`, `regression`, `cleanup` and others, executed in a defined order), and `when` guards a stage with conditions. Scripted is older and unrestricted: it is Groovy, so loops, try/catch, functions, and arbitrary logic are available everywhere; the `node {}` block schedules the work on an executor and creates a workspace. `stage` blocks are optional in Scripted — they exist mostly for UI visualization — while they are mandatory containers in Declarative. Both feed the same tool-neutral model of [[What is a CI CD pipeline]]; only the authoring style differs.

```java
// Conceptual: the same flow in both syntaxes
// Declarative
pipeline {
    agent any
    stages {
        stage('Build') { steps { sh 'make' } }
    }
    post { always { junit 'reports/**/*.xml' } }
}

// Scripted equivalent
node {
    stage('Build') { sh 'make' }
    junit 'reports/**/*.xml'
}
```

**Listing 1.** Identical semantics: Declarative prescribes the skeleton; Scripted is Groovy with optional stage markers.

## Where each syntax earns its keep

Declarative is the default recommendation for team-owned pipelines: the fixed skeleton makes every Jenkinsfile in the company look alike, review focuses on logic, and the shared vocabulary (`agent`, `post`, `when`) maps onto documentation and the directive generator. Scripted earns its keep where pipeline logic is genuinely programmatic — dynamic matrix generation, complex branching, custom retry policies — and inside Shared Libraries, where the reusable steps are usually written as Groovy functions regardless of the caller's syntax. The two mix in practice: Declarative pipelines escape into Groovy through `script { }` blocks when the rigid sections run out.

> [!warning] Two persistent myths
> "Declarative replaced Scripted" is false — both are supported, and no deprecation exists; the docs explicitly present them as two syntaxes of the same subsystem. The mirror myth — "Declarative cannot do loops or conditionals" — is also false: `when` covers stage conditions, and `script { }` admits Groovy where needed. The real trade-off is the opposite direction: unrestricted Groovy in Scripted pipelines is how teams end up with unmaintainable, unreviewable build code; also note a known Declarative limitation on the maximum size of code inside the `pipeline {}` block, which does not apply to Scripted — a rare but real reason to split or switch.

> [!tip] Interview answer
> **Declarative is the structured syntax — a mandatory pipeline block with agent, stages, post, and when directives, validated before execution, uniform across teams. Scripted is plain Groovy in node blocks: imperative, maximally flexible, with stages optional and no structural validation. They share the same steps and both exist since Pipeline plugin 2.5; neither is deprecated. Default to Declarative for readability, drop to Groovy via script blocks or Shared Libraries when logic is genuinely programmatic.**
