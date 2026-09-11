<!--
reps: 0
priority: 0
-->
#Methodologies/TDD #SRS

# How would you explain Test-Driven Development?

> [!abstract] Short answer
> TDD is a development technique, created by Kent Beck in the late 1990s as part of Extreme Programming, where you drive implementation by writing tests first: write a failing test for the next bit of behavior, write just enough production code to pass it, then refactor. The cycle is known as red-green-refactor, and Martin Fowler defines the technique plainly - "building software that guides software development by writing tests".

## The loop in practice

Fowler's canonical description has three repeated steps - "write a test for the next bit of functionality you want to add; write the functional code until the test passes; refactor both new and old code to make it well structured" - plus a vital preliminary: write out a list of test cases first, then pick one at a time, choosing tests that "drive us quickly to the salient points in the design". Red means the test fails for the expected reason (proving it tests something). Green means passing by the simplest honest implementation - hard-coding a return value is a legitimate green step if the next test forces generalization. Refactor removes duplication and clarifies names with the safety net on. XP's second edition calls the practice Test-First Programming ([[Why does TDD write tests before production code]]).

```d2
direction: down
list: "1. List test cases" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
pick: "2. Pick one test" {
  width: 260
  height: 55
}
red: "3. RED: run, watch it fail" {
  width: 300
  height: 55
  style.fill: "#fde8e8"
}
green: "4. GREEN: minimal code to pass" {
  width: 310
  height: 55
  style.fill: "#e8f5e9"
}
ref: "5. REFACTOR: clean code, stay green" {
  width: 310
  height: 55
  style.fill: "#fff3e0"
}
list -> pick -> red -> green -> ref
ref -> pick: "next test"
```

**Fig. 1.** TDD as Fowler describes it: the list of test cases up front, then the red-green-refactor loop per test.

## What people get wrong

The classic failure, per Fowler, is "neglecting the third step" - skipping refactoring and accumulating "a messy aggregation of code fragments" that happens to have tests. The second: writing five tests before any code, breaking the feedback loop that makes TDD valuable. The third: testing implementation details (private methods, exact call sequences) instead of behavior, which turns the suite into a brake on refactoring. BDD grew out of exactly this confusion - Dan North designed it to answer "where to start, what to test and what not to test, how much to test in one go, what to call their tests" ([[How would you explain behavior driven development BDD]]).

> [!warning] TDD is not "we have high coverage"
> Coverage is an output, not the goal; a suite written after the fact can hit high coverage with no design benefit, and a TDD suite can still assert the wrong behavior. The tell of real TDD is process: tests exist before the code they specify, the loop is minutes long, and refactoring happens under green. If the team writes code first and backfills tests to hit a coverage number, that is test-last with extra steps ([[What is refactoring]]).

> [!tip] Interview answer
> TDD means the test defines the next behavior before the code exists: red for the right reason, green by the simplest honest implementation, then refactor under the safety net, with a list of upcoming tests guiding the order. Kent Beck introduced it in XP; Fowler's summary is the standard one. The point is not coverage - it is interface-first design and a suite that makes continuous refactoring safe.
