<!--
reps: 0
priority: 0
-->
#Java/Testing #SRS

# How would you explain AssertJ vs Hamcrest

> [!abstract] Short answer
> **Both are assertion libraries; the difference is the API shape.** Hamcrest is matcher-based: `assertThat(actual, matcher(x))` — declarative, composable, but the failure messages and discoverability lag behind. AssertJ is fluent: `assertThat(actual).isEqualTo(x).hasSize(3)` — chainable, type-aware per JDK type, with error messages that print the actual value and collection contents.

## Two shapes for the same check

Hamcrest's `assertThat` comes from `MatcherAssert` and takes a `Matcher<T>`; the matcher decides pass/fail and describes the expectation. AssertJ's `assertThat` returns a typed assert object (`StringAssert`, `ListAssert`) whose methods both check and return `this`, enabling chains. Same checks, different ergonomics:

```d2
direction: right
h: "Hamcrest\nassertThat(x, equalTo(y))\nmatcher decides + describes" {
  width: 300
  height: 100
  style.fill: "#e3f2fd"
}
a: "AssertJ\nassertThat(x).isEqualTo(y)\nreturns this -> chaining" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
h2: "Composable matchers:\nallOf / anyOf / not" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
a2: "Type-aware API per class:\nstartsWith, hasSize, extracting" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
h -> h2
a -> a2
```

**Fig. 1.** Hamcrest puts the logic in reusable `Matcher` objects; AssertJ puts it in methods of the returned assert class.

```java
String name = "Frodo";
Integer[] bag = {1, 2, 3};

// same check, two styles
assertThat(name).startsWith("Fro").endsWith("do").hasSize(5);
assertThat(name, allOf(startsWith("Fro"), endsWith("do")));

assertThat(bag).hasSize(3).contains(1, 3).doesNotContain(9);
assertThat(bag, allOf(hasItemInArray(1), hasItemInArray(3)));
```

**Listing 1.** A fluent chain reads left-to-right; Hamcrest nests combinators. Both pass.

## What the failure messages look like

The failure message is where teams usually pick. Run both assertions against a wrong expectation and compare:

```java
try {
    assertThat("chocolate chips", bag.length, equalTo(10));
} catch (Throwable e) {
    System.out.println("Hamcrest:");
    System.out.println(e.getMessage().trim());
}
try {
    assertThat(bag).as("bag contents").hasSize(10);
} catch (Throwable e) {
    System.out.println("AssertJ:");
    System.out.println(e.getMessage().trim());
}
```

**Listing 2.** Caught failures, printed verbatim on JDK 21:

```java
Hamcrest:
chocolate chips
Expected: <10>
     but: was <3>
AssertJ:
[bag contents]
Expected size: 10 but was: 3 in:
[1, 2, 3]
```

**Listing 3.** AssertJ prints the actual collection contents and honors the `.as(...)` description; Hamcrest prints the description on its own line plus expected/but.

> [!warning] Two traps people hit in interviews
> First, Hamcrest is NOT an assertion engine by itself — `assertThat` delegates to JUnit/AssertJ-free `MatcherAssert`, and mixing `org.hamcrest` and `org.junit` `assertThat` overloads is a classic compile-error source. Second, Hamcrest's matchers fight Java generics around primitive arrays: `assertThat(int[], hasItemInArray(1))` does not compile — you need `Integer[]` or collection matchers, while AssertJ's `assertThat` overloads accept the array directly. Neither library runs real code: they only compare values, so neither replaces a mock — see [[What is the difference between Mock and MockBean]].

## Choosing in a real project

AssertJ is the de-facto choice for new JUnit 5 code: type-discoverable chains, `extracting(...)` for field projections, soft assertions collected into one report (see [[What is the difference between hard and soft assertions]]), and `assertThatThrownBy` for exceptions. Hamcrest remains worth knowing because it is the lingua franca of matcher APIs — Mockito's argument matchers, WireMock's request predicates and Spring's test matchers copy its style. Baseline JUnit assertions are covered by [[Which assertions does JUnit provide]].

> [!tip] Interview answer
> **Hamcrest is matcher-style: assertThat(actual, matcher) with composable matchers like allOf — declarative but weak messages and generic friction. AssertJ is fluent: assertThat(actual).isEqualTo(...).hasSize(...) chains, typed per JDK class, with failure messages that show actual contents and support soft assertions and extracting. New code defaults to AssertJ; Hamcrest matters because many libraries borrow its matcher style.**

