<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# What are the phases of the three Maven lifecycles

> [!abstract] Short answer
> **The default lifecycle is 23 phases from `validate` to `deploy`; clean has three (`pre-clean`, `clean`, `post-clean`); site has four (`pre-site`, `site`, `post-site`, `site-deploy`).** Which goals actually run at each default-lifecycle phase depends on the packaging — the `jar` packaging binds resources, compiler, surefire, and jar goals; the `pom` packaging binds only `install` and `deploy`.

The familiar headline phases (`validate`, `compile`, `test`, `package`, `verify`, `install`, `deploy`) are a compressed view. The full default chain interleaves `generate-*`, `process-*`, and `prepare-` steps that exist so plugins can inject material into the build: sources generated before `compile`, resources filtered in `process-resources`, bytecode enhanced in `process-classes`, packages prepared in `prepare-package`. The clean lifecycle is `pre-clean → clean → post-clean`; the site lifecycle is `pre-site → site → post-site → site-deploy`, and it is the only lifecycle whose end point publishes to a server rather than a repository ([[What are Maven plugins and how are goals invoked]] explains who executes a phase).

## The full default sequence and the jar bindings

```text
validate, initialize, generate-sources, process-sources,
generate-resources, process-resources, compile, process-classes,
generate-test-sources, process-test-sources, generate-test-resources,
process-test-resources, test-compile, process-test-classes, test,
prepare-package, package, pre-integration-test, integration-test,
post-integration-test, verify, install, deploy
```

**Listing 1.** All 23 default-lifecycle phases in execution order — invoking any one of them runs the prefix up to it ([[How would you explain the Maven build lifecycle]]).

For the `jar` packaging the built-in bindings are: `resources:resources` at process-resources, `compiler:compile` at compile, `resources:testResources` at process-test-resources, `compiler:testCompile` at test-compile, `surefire:test` at test, `jar:jar` at package, then `install:install` and `deploy:deploy`. Hyphenated phases — the `pre-*`, `post-*`, `process-*`, `generate-*`, and `prepare-*` names — are not meant to be called from the command line: they sequence the build and produce intermediate results. A phase with no bound goals does nothing, which is why `pom`-packaged projects (pure metadata: parents, BOMs) finish a "build" after just two goal executions.

> [!warning] Stopping at `integration-test` leaves wreckage
> Running `mvn integration-test` instead of `mvn verify` is the classic operational trap: goals bound to `pre-integration-test` have started containers or servers, and the teardown goals live in `post-integration-test` — which never runs because the build stops (or crashes) mid-phase. The environment hangs, and reports bound to `verify` are never generated. Always call `verify` to let the lifecycle unwind; the Failsafe story is in [[What is the difference between the Surefire and Failsafe plugins in Maven]].

> [!tip] Interview answer
> **Default has 23 phases — validate through deploy, with generate/process/prepare steps for plugin injection; clean has three, site has four including site-deploy. The packaging decides which goals fire: jar packaging binds compiler, surefire, jar, install, deploy goals; pom packaging only install and deploy. Never stop the command at integration-test — containers started for it get torn down after it, so you call verify.**
