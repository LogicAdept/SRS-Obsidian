<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS

# What is `@DirtiesContext`?

> [!abstract] Short answer
> **`@DirtiesContext`** tells TestContext that this test **dirtied** the `ApplicationContext` (typical case: **mutated a singleton**). The framework **removes that context from the static cache and closes it**. The next test that needs the **same** configuration **rebuilds** a fresh container. It is a class- or method-level annotation, not a transaction rollback.

## When the cache is dropped

Support is `DirtiesContextBeforeModesTestExecutionListener` and `DirtiesContextTestExecutionListener` (both on by default). After eviction, the following test with that `MergedContextConfiguration` pays a **full refresh**. Prefer [[What is the difference between DirtiesContext and Transactional in tests]] for database isolation — rollback **keeps** the cached context. Overview: [[What is the Spring TestContext Framework]]. Cache key: [[How does the Spring TestContext framework cache the ApplicationContext]].

**Class-level `classMode` (default `AFTER_CLASS`):**

| `classMode` | When the context is marked dirty |
| --- | --- |
| `BEFORE_CLASS` | Before the test class |
| `AFTER_CLASS` | After the test class (**default**) |
| `BEFORE_EACH_TEST_METHOD` | Before **every** method in the class |
| `AFTER_EACH_TEST_METHOD` | After **every** method in the class |

**Method-level `methodMode` (default `AFTER_METHOD`):** `BEFORE_METHOD` or `AFTER_METHOD`. Class and method annotations on the same test are **both** honored (for example class `BEFORE_EACH_TEST_METHOD` plus method `AFTER_METHOD` dirties **before and after** that method).

```java
@DirtiesContext
class ContextDirtyingTests {
	// dirty after the class (default classMode = AFTER_CLASS)
}

@Test
@DirtiesContext
void testProcessWhichDirtiesAppCtx() {
	// dirty after this method (default methodMode = AFTER_METHOD)
}
```

**Listing 1.** Official default modes. `AFTER_EACH_TEST_METHOD` is a **classMode**, not the method default.

## Hierarchies

With [[What is ContextHierarchy]], `hierarchyMode` defaults to **`EXHAUSTIVE`**: clear the current level **and** every cached hierarchy that shares a **common ancestor**, closing all `ApplicationContext`s in those sub-trees. **`CURRENT_LEVEL`** closes only the current level.

```java
@ContextHierarchy({
	@ContextConfiguration("/parent-config.xml"),
	@ContextConfiguration("/child-config.xml")
})
class BaseTests {}

class ExtendedTests extends BaseTests {

	@Test
	@DirtiesContext(hierarchyMode = DirtiesContext.HierarchyMode.CURRENT_LEVEL)
	void test() {
		// child dirtied; do not evict every cousin that shares the parent
	}
}
```

**Listing 2.** Conceptual: current-level algorithm when only the child is corrupted.

```d2
direction: down
test: "test mutates a singleton" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
dirty: "@DirtiesContext" {
  width: 200
  height: 40
  style.fill: "#ffebee"
}
cache: "remove + close\nstatic ContextCache" {
  width: 240
  height: 50
  style.fill: "#fce4ec"
}
next: "next same-key test\nrebuilds ApplicationContext" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

test -> dirty
dirty -> cache
cache -> next
```

**Fig. 1.** Dirty means **close**, not “skip DI.” LRU eviction (default max 32) also closes contexts, but that is size pressure, not this annotation.

> [!warning]Class default is AFTER_CLASS not every method
> Bare `@DirtiesContext` on a **class** runs **once after the class**, not after each `@Test`. After-each-method is **`classMode = AFTER_EACH_TEST_METHOD`**. Bare `@DirtiesContext` on a **method** is **`AFTER_METHOD`**. Interview mix-up of those three names is common.

> [!warning]Exhaustive mode closes cousin hierarchies
> Default **`hierarchyMode = EXHAUSTIVE`** can drop **parent** and **other children** that share an ancestor, which is far more expensive than `CURRENT_LEVEL`. Do not use `@DirtiesContext` as a substitute for `@Transactional` rollback.

> [!tip] Interview answer
> **`@DirtiesContext` evicts and closes the cached `ApplicationContext` because the test mutated it.** Class default is after the class; method default is after the method. `AFTER_EACH_TEST_METHOD` is a class mode. In a `@ContextHierarchy`, exhaustive mode also clears related ancestor trees. It is the expensive hammer; transactions are for data, not for this.
