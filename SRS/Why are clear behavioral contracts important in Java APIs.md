<!--
reps: 0
priority: 0
-->
#Methodologies/DesignByContract #SRS

# Why are clear behavioral contracts important in Java APIs?

> [!abstract] Short answer
> Because a Java API is used by people who cannot see its implementation: what keeps their code correct is the documented contract - what a method requires from the caller, what it guarantees on return, which exceptions mean what, under what conditions behavior is defined. Java's standard library is built on precisely specified contracts (`Objects.requireNonNull`, the `equals`/`hashCode` pair, `Iterator.next` throwing `NoSuchElementException`), and APIs with vague contracts force every client into defensive guesswork - or into bugs that appear only with a different implementation.

## What a contract protects on each side

The caller gets a promise: given these preconditions, this postcondition holds and these exceptions carry these meanings - so client code can be written once and reasoned about locally. The implementer gets freedom: any implementation satisfying the contract is valid, which is what allows swapping implementations, optimizing, or subclassing without breaking clients. The JDK's own contracts are the canonical examples: `equals` must be reflexive, symmetric, transitive, consistent, and `x.equals(y)` implies `x.hashCode() == y.hashCode()` ([[What is the Object equals contract]], [[How would you explain the equals and hashCode contract together in Java]]); `Iterator.next` promises the next element or `NoSuchElementException` - and never returns null for exhausted iterators. Break the contract and every client that trusted it breaks with it.

```java
/**
 * @throws IllegalArgumentException  if freq <= 0 (precondition: caller's duty)
 * @return  a sampler yielding values with the given frequency
 *          (postcondition: implementer's promise)
 */
public Sampler newSampler(int freq) {
    if (freq <= 0) throw new IllegalArgumentException("freq must be positive");
    ...
}
```

**Listing 1.** Conceptual. The contract is visible at the signature level: fail fast on precondition violation, and guarantee the documented result for every valid call.

## The system-level payoff

Clear contracts are what make abstraction and substitution safe: they are the specification that lets a different implementation drop in - the API-design twin of the Liskov substitution rule. They localize errors: a violated precondition throws at the faulty caller instead of surviving as corrupted state that explodes three layers later. And they shrink defensive programming: without a stated contract, every client over-checks (or under-checks); with one, checks live at the boundary that owns them. This is Design by Contract thinking applied with Java's tools - documented preconditions, checked exceptions with defined meanings, immutable value types - even where the language lacks native DbC support ([[How would you explain programming by contract and preconditions]]).

> [!warning] "The Javadoc is the contract" only if it constrains, not describes
> Documentation that merely narrates the implementation ("increments the counter and returns it") is not a contract; the contract states obligations and guarantees ("the counter never decreases; returns are monotonic"). The second trap: hidden contracts - behavior clients discover by accident (map iteration order for a HashMap) and then depend on; when the implementation changes, they break. State the contract deliberately, and mark what is explicitly NOT guaranteed ([[What is the Object equals contract]]).

> [!tip] Interview answer
> Contracts are what let Java APIs be used without reading implementations: preconditions the caller must meet, guarantees the implementer must keep, exceptions with defined meanings. The JDK's equals-hashCode and iterator contracts show the model working at scale. Clear contracts enable safe substitution, fail-fast error localization, and less defensive code - and I treat vague or accidental behavior as a design defect, not documentation debt.
