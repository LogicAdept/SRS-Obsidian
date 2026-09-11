<!--
reps: 0
priority: 0
-->
#Methodologies/BDD #SRS

# How would you explain behavior driven development BDD?

> [!abstract] Short answer
> BDD is Dan North's evolution of TDD that reframes testing as specifying behavior in business terms. Instead of "test", you talk about behavior examples; test names become full sentences describing what the system does; scenarios follow a given-when-then template that business people can read. North introduced it after watching teams struggle with TDD mechanics - "where to start, what to test and what not to test, how much to test in one go, what to call their tests, and how to understand why a test fails" - and it has since grown, in his words, into "the wider picture of agile analysis and automated acceptance testing".

## Where it came from

North's original article tells the origin honestly. The first trigger was a utility called agiledox by Chris Stevenson that printed JUnit test method names as plain sentences - suddenly a test named `shouldRejectOverdrawnAccount` read like a specification, and the "test" framing was exposed as the problem. The second was business analyst Chris Matts pushing business value into the loop: prioritize by asking "what is the next most important thing the system doesn't do". The result: BDD reuses TDD's mechanics but changes the vocabulary and the questions - methods named as sentences with "should", behaviors prioritized by value, and examples written in a given-when-then structure.

```gherkin
Scenario: Overdraft limit blocks withdrawal
  Given an account with balance 50 and an overdraft limit of 100
  When the customer withdraws 120
  Then the withdrawal is declined
  And the balance remains 50
```

**Listing 1.** Conceptual. A scenario in the given-when-then shape: initial context, the event, the expected outcomes. The same text is a review artifact for the analyst and an executable test fixture for the engineer.

## What BDD changes in the workflow

Three practices distinguish it from plain TDD. Outside-in: start from an acceptance behavior at the system boundary and let failing scenarios pull implementation down through layers, rather than inventing internals first. Shared examples: scenarios live in a form the business can review - tools such as JBehave and Cucumber execute such texts against the system - so acceptance criteria become automated and non-programmers can read (and challenge) them. Language discipline: "should" instead of assertion-speak, behavior names instead of method names, a shared vocabulary with the business that mirrors what DDD calls ubiquitous language ([[What is ubiquitous language and why does it matter]]).

> [!warning] BDD is not "TDD with a cucumber logo"
> Automating scenarios in a Gherkin dialect while analysts and business never see them is tool worship, not BDD - the point of the readable layer is the shared conversation, not the parser. The second trap: wrapping every unit test in given-when-then; North's practices are aimed at behavior and acceptance, and forcing the template onto low-level tests adds ceremony with no shared understanding gained. TDD still drives the inner loop ([[How would you explain Test-Driven Development]]) - BDD organizes the outer, business-facing one.

> [!tip] Interview answer
> BDD is Dan North's answer to TDD's adoption pains: describe behavior as sentences and given-when-then examples that the business can read, drive work by business value, and automate those examples as acceptance tests. I present it as TDD's outer layer - same red-green engine inside, but the requirements conversation moves to a language shared with non-programmers, which kills a whole class of misunderstanding bugs.
