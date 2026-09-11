<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/SOLID #SRS

# How would you explain the Interface Segregation Principle in SOLID?

> [!abstract] Short answer
> ISP says clients should not be forced to depend on methods they do not use. Robert Martin introduced it in 1996 after watching "fat" interfaces - one big interface serving every client - force innocent consumers to recompile, redeploy, and even reimplement because of changes they never cared about. The fix is segregating by client role: many small, purpose-specific interfaces instead of one kitchen-sink contract, so each client depends only on the slice it actually calls.

## The mechanism: fat interfaces couple everyone to everything

When an interface accumulates methods for all its consumers, two failure modes follow. Static: a change to a method that client A never uses still changes the interface A depends on, so A recompiles and redeploys for nothing - the dependency is real even when the call is absent. Dynamic: implementations must supply bodies for methods they do not support, and the classic stink appears - `UnsupportedOperationException` thrown from half of an implementation. Segregation cuts the contract into role-shaped pieces: `Readable`, `Writable`, `Closeable` - clients type their dependencies to the smallest role they use.

```d2
direction: down
fat: "Worker interface\ndoWork + sleep + eat + backup" {
  width: 320
  height: 70
  style.fill: "#fde8e8"
}
robot: "Robot impl\nthrows on sleep, eat" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
human: "Human impl\nthrows on backup" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
roles: "Segregated: Workable, Restable, Backupable" {
  width: 360
  height: 60
  style.fill: "#e8f5e9"
}
fat -> robot
fat -> human
fat -> roles: "segregate by client role"
```

**Fig. 1.** The fat interface forces impossible methods on every implementer; role interfaces give each client and implementer only its own slice.

## Where it shows up in Java

Java's own library is a masterclass in ISP by another name: `Observer`/`Observable` roles, `Comparable` vs `Comparator`, `Readable`/`Appendable` splitting reading from writing - small contracts that compose. Java 8 default methods weakened the historical cost of fat interfaces (implementers no longer must write stub bodies), and that convenience quietly reintroduced the temptation: one wide `interface` with default no-ops instead of genuine segregation - the static coupling never went away; only the compiler's complaint did. For tests, ISP pays visibly: faking a two-method role interface is trivial, faking a forty-method god interface is why teams reach for mocking frameworks ([[What is Observer]], [[How would you explain the SOLID design principles as a set]]).

> [!warning] "Many tiny interfaces everywhere" is not ISP either
> Segregation is BY CLIENT ROLE - cut along the lines clients actually consume, and no finer. An interface per method with no role behind it just scatters one concept and forces adapters between slices; a method used by every client in one role belongs in that role's interface. The second trap: fixing a fat interface in the wrong direction - adding default bodies to silence implementers instead of splitting the contract leaves the coupling intact ([[What can violating SOLID principles lead to]]).

> [!tip] Interview answer
> ISP: clients depend only on methods they use - so segregate fat interfaces into role-shaped contracts. The costs of skipping it are recompiles and forced stub implementations whenever someone else's feature changes the shared contract. I keep interfaces small on purpose, like Readable and Appendable in the JDK, and I treat UnsupportedOperationException in an implementation as the smell that a contract needs splitting.
