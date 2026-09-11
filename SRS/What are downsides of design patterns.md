<!--
reps: 0
priority: 0
-->
#Patterns/GoF #Patterns/AntiPatterns #SRS

# What are downsides of design patterns

> [!abstract] Short answer
> The three standard criticisms: patterns can be **workarounds for missing language features**, they get applied **dogmatically** where a simpler solution fits, and beginners **overuse them** ("if all you have is a hammer"). On top of that, every pattern adds classes and indirection, and some — like Singleton — bring well-known structural damage.

## The three standard criticisms

First, a pattern often exists because a language lacks an abstraction. The usual example is Strategy: in modern languages with function types, it shrinks from an interface plus strategy classes to a plain lambda, so the "pattern" was a kludge compensating for the language. Paul Graham made this point generally: the need for patterns arises when the chosen technology lacks the required level of abstraction. Second, patterns systematize practices that already worked, and treating that systematization as dogma produces inefficient solutions — teams follow the catalog to the letter instead of adapting the idea to the project. Third, unjustified use: people who just learned patterns try to apply them everywhere, even where simpler code would do fine.

## The practical cost in code

Independently of the criticisms, each pattern has a mechanical price. Most of them introduce extra interfaces, classes, and delegation layers, so the overall complexity grows — that is the explicit con listed for Builder, Adapter, Command, and Proxy in the classic catalog. Singleton carries its own list: hidden global state, components that know too much about each other, and hard-to-mock clients, which is why [[Why is the singleton pattern often labeled an anti pattern]] is a fair question and not just provocation.

> [!warning] "A pattern always improves the design" is a lie
> If a lambda, a plain field, or a single method solves the problem, adding a formal pattern is a net loss: more code, more indirection, zero new capability. See [[What is a lightweight alternative to the Command pattern]] for a case where the pattern often should collapse.

> [!tip] Interview answer
> The main downsides: patterns can be compensations for weak language abstractions, so modern language features remove some of them; applied dogmatically they produce bloated, inefficient code; and beginners overuse them where simple code fits. Mechanically they add classes and indirection, and Singleton in particular brings global-state and testability problems.
