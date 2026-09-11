<!--
reps: 0
priority: 0
-->
#Methodologies/TDD #SRS

# Why does TDD write tests before production code?

> [!abstract] Short answer
> Because the test written first is a specification of what you are about to build, not a chore bolted on afterwards. It forces you to think about the interface before the implementation, it gives you an immediate executable definition of "done", and it leaves behind self-testing code that catches regressions for the rest of the project's life. Martin Fowler's summary of the two test-first benefits is exactly this: you get self-testing code, and "thinking about the test first forces us to think about the interface to the code first".

## The mechanism of the benefit

Test-after testing measures code that already exists, and it quietly inherits the shape of the implementation: you test the methods you happened to write. Test-first inverts the flow - you describe the next piece of behavior from the caller's seat, watch it fail (red), write just enough code to pass (green), then restructure (refactor). Each cycle is seconds to minutes long, so feedback is immediate: a wrong assumption costs one small step, not an integration phase. Over hundreds of cycles this compounds into two structural effects: the API gets shaped by its first client (the test), and the suite grows one case per behavior with no "we'll add tests later" debt ([[How would you explain Test-Driven Development]]).

```d2
direction: right
red: "RED\nwrite a failing test" {
  width: 220
  height: 75
  style.fill: "#fde8e8"
}
green: "GREEN\nmake it pass simply" {
  width: 220
  height: 75
  style.fill: "#e8f5e9"
}
ref: "REFACTOR\nclean both sides" {
  width: 220
  height: 75
  style.fill: "#e3f2fd"
}
red -> green -> ref -> red: "minutes per cycle"
```

**Fig. 1.** The red-green-refactor loop. The refactoring leg is part of the loop - skipping it is, per Fowler, "the most common way that I hear to screw up TDD".

## The benefits interviewers expect, in order

First: interface-first thinking - the test is the first client, so awkward APIs hurt immediately, before consumers exist. Second: a regression safety net - self-testing code makes refactoring safe, which is what keeps a codebase changeable ([[What is refactoring]]). Third: fast, precise failure localization - a red test names the behavior that broke. Fourth: executable specification - the suite documents behavior with examples, and "done" stops being a matter of opinion. Fifth: design pressure toward testability - code that is hard to test is usually hard to compose, and the loop surfaces that within minutes ([[How can you test a program and reduce the risk of bugs]]).

> [!warning] "Tests first" does not mean "test everything first"
> The discipline is one test, then code, in a tight loop - not a two-week test-writing phase before any implementation, which is just BDUF with assertions. The second lie: TDD guarantees good design. It guarantees coverage of the behavior you thought to specify; design still requires the refactoring leg and judgment. A suite can also ossify a bad interface - if the first test encoded a poor API, tests-first makes it sticky; fixing that means changing the test deliberately, not obediently keeping it green ([[Why does TDD write tests before production code]]).

> [!tip] Interview answer
> Test-first turns the test into a specification: I define the next behavior, see it fail, then make it pass. That ordering buys interface-first design, immediate feedback, and a self-testing suite that makes refactoring safe - coverage is a side effect, the real product is the design loop. And I keep the cycle minutes long, because the value is in the feedback, not in the ceremony.
