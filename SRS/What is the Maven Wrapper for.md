<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# What is the Maven Wrapper for

> [!abstract] Short answer
> **It encapsulates the build: `./mvnw` runs Maven at exactly the version pinned in the project's `.mvn/wrapper/maven-wrapper.properties`, downloading that distribution first if it is missing.** Contributors and CI need no pre-installed Maven — the required version travels with the project, so everyone builds with the same toolchain.

## How it works

The wrapper plugin generates the files: `mvnw` (a POSIX shell script), `mvnw.cmd` for Windows, and the properties file `.mvn/wrapper/maven-wrapper.properties` recording the pinned distribution. By default the `only-script` type is installed — no binary jar in the repo; the older `bin` type adds a small `maven-wrapper.jar` that bootstraps the download instead. On first run the script checks for the pinned version, downloads and installs it if absent, then executes the ordinary build; later runs reuse the already-downloaded distribution. The wrapper itself works with any Maven 3.x or later and defaults to the release that was active when the wrapper was set up.

```java
# one-time setup (or version bump) — committed to VCS
mvn wrapper:wrapper

# everyone, including CI, runs the build through the scripts
./mvnw clean install
mvnw.cmd clean install
```

**Listing 1.** The documented setup and usage: `wrapper:wrapper` writes or updates the wrapper files, and the scripts replace plain `mvn` in every instruction, README, and CI pipeline.

```d2
direction: right
inv: "./mvnw clean install" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
props: "maven-wrapper.properties\npinned distribution" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
dl: "Download + install\nif version missing" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
build: "Run the build\nat the pinned version" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
inv -> props
props -> dl: "not installed yet"
dl -> build
props -> build: "already present"
```

**Fig. 1.** The properties file is the contract: same project, same Maven version, on every machine and in every CI job.

> [!warning] The wrapper pins Maven — nothing else
> Interview and practice trap number one: assuming the wrapper makes builds reproducible. It pins only the build tool; plugin and dependency versions still drift unless they are managed — a pinned Maven downloading unpinned artifacts is not reproducible. Trap two: the project says `./mvnw` but a developer runs a globally installed `mvn` with a different version and gets subtly different behavior — new plugin defaults, different resolution — which is why team convention is that the wrapper scripts are the only documented way to invoke the build. And since the pinned version is checked into the repository, a wrapper bump is a reviewable, bisectable change — treat a silent local edit of the properties file as what it is: a fork of the toolchain. Where wrapper versions sit next to dependency pinning: [[What is the dependencyManagement section in Maven for]]; the day-to-day command the scripts wrap: [[How would you explain mvn clean install]]; what CI needs from a build tool contract: [[Which CI CD tools do you know]].

> [!tip] Interview answer
> **The Maven Wrapper commits the build tool into the project: mvnw scripts plus a properties file pin the exact Maven distribution, and on first run it downloads that version if missing. So contributors and CI need no global install and everyone runs the same Maven. I commit it to VCS, I bump it deliberately like any dependency, and I remember it pins only the tool — plugins and libraries still need managed versions for true reproducibility.**

