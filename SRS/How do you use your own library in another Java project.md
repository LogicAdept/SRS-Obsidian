<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #Build/ArtifactRepositories #SRS

# How do you use your own library in another Java project

> [!abstract] Short answer
> **Publish the library into a Maven repository and depend on it by coordinates from the other project.** Locally: `mvn install` on the library puts it into `~/.m2/repository`, where sibling projects resolve it. For a raw third-party jar: `mvn install:install-file`. For team-wide sharing: `mvn deploy` to an internal repository (Nexus/Artifactory) once — never pass jars around by hand.

## Three levels of publishing

First, the normal case — the library is itself a Maven project. Running the `install` phase packages it and copies the artifact plus its POM into the local repository under its coordinates, so any project on the machine can declare `groupId:artifactId:version` and resolve it. Second, a vendor jar that has no Maven build at all: the install plugin's `install-file` goal places it manually. Third, making the library available to the whole team: deploy pushes it to a remote, internal repository, and consumers resolve it like any other artifact.

```java
# a Maven-built library: one phase does it
mvn clean install

# a bare vendor jar, placed by coordinates
mvn install:install-file -Dfile=acme-2.3.jar \
    -DgroupId=com.acme -DartifactId=acme-core \
    -Dversion=2.3 -Dpackaging=jar

# team-wide: push to the internal repository
mvn deploy:deploy-file -Dfile=acme-2.3.jar \
    -DgroupId=com.acme -DartifactId=acme-core -Dversion=2.3 -Dpackaging=jar \
    -DrepositoryId=internal-releases \
    -Durl=https://nexus.example.com/repository/releases/
```

**Listing 1.** Canonical forms from the Maven guides for installing third-party JARs: `install-file` for the local cache, `deploy:deploy-file` for the team repository. `-DrepositoryId` names a `<server>` entry in `settings.xml` that carries the credentials.

```d2
direction: right
lib: "Library project\nmvn clean install" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
local: "Local repository\n~/.m2/repository" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
remote: "Internal repository\nNexus / Artifactory" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
app: "Other projects\ndepend by coordinates" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
lib -> local: "install phase"
local -> app: "resolve locally"
remote -> app: "resolve remotely"
lib -> remote: "mvn deploy (team-wide)"
```

**Fig. 1.** Two publishing targets, one consumption contract: coordinates. Local `install` serves the machine; `deploy` to an internal repository serves the team.

A Maven-built jar carries its own POM inside `META-INF/maven/`, so a recent install plugin reads the coordinates from the jar itself and `install-file` needs only `-Dfile`. If a POM exists separately, pass `-DpomFile`; on the deploy side, `deploy-file` generates a generic POM unless told otherwise (`-DgeneratePom=false` or `-DpomFile`).

> [!warning] install is machine-local, and system-scope jars are the anti-pattern to refuse
> The recurring interview lie: "I installed the jar, so the team can use it." The `install` phase writes to your personal `~/.m2` — nothing is shared. Team sharing means a deployed artifact on a repository manager. The other classic: checking jars into version control and wiring them with `system` scope and a hardcoded path — Maven does not download system-scoped jars, the path breaks on every other machine, and the official recommendation is a private hosted repository instead; a real repository keeps coordinates, versions, and transitive metadata intact. And when builds act haunted after a botched `install-file` with wrong coordinates, remember the local repository is just a cache — delete the bad directory and reinstall. Resolution mechanics: [[How does Maven resolve artifacts from repositories]]; what `install` does phase-wise: [[How would you explain mvn clean install]]; why scope choice matters on the consumer side: [[What are the dependency scopes in a Maven pom]].

> [!tip] Interview answer
> **For local development, mvn clean install on the library — or install-file for a bare vendor jar — publishes it to ~/.m2 by coordinates, and the other project just declares the dependency. For the team, deploy once to an internal repository like Nexus with credentials from settings.xml, and everyone resolves it normally. I never commit jars or use system scope — the repository is the single source of artifacts.**

