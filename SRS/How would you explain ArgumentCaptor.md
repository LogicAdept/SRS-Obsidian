<!--
reps: 0
priority: 0
-->
#Java/Testing/Mockito #SRS

# How would you explain ArgumentCaptor

> [!abstract] Short answer
> **ArgumentCaptor is a Mockito hook that records the real arguments a mock received, so you can assert on them after verification.** You write `captor.capture()` where the expected argument would stand, run `verify`, then read `getValue()` or `getAllValues()` and assert with your favorite assertion library.

## Capture during verify

A plain `verify(mock).save(new User("Alice", 30))` checks equality against a hardcoded value. ArgumentCaptor flips that: instead of providing the expected value, you let Mockito hand you the actual one.

```d2
direction: right
call: "Test calls\nservice.register(\"Alice\", 30)" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
mock: "Mocked repo\nrecords the User instance" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
verify: "verify(repo).save(\ncaptor.capture())" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
assert: "captor.getValue()\n-> assert on fields" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
call -> mock
mock -> verify
verify -> assert
```

**Fig. 1.** The captor does not intercept anything at call time — it is an argument placeholder whose value is filled in when the `verify` runs.

```java
record User(String name, int age) {}
interface UserRepository { void save(User user); }

UserRepository repo = mock(UserRepository.class);
new UserService(repo).register("Alice", 30);

ArgumentCaptor<User> captor = ArgumentCaptor.forClass(User.class);
verify(repo).save(captor.capture());
User saved = captor.getValue();
System.out.println("captured: " + saved.name() + " / " + saved.age());

new UserService(repo).register("Bob", 41);
verify(repo, times(2)).save(captor.capture());
System.out.println("all: " + captor.getAllValues());
```

**Listing 1.** Capture one value, then re-capture across two invocations. Output on JDK 21 with Mockito 5.11:

```java
captured: Alice / 30
all: [User[name=Alice, age=30], User[name=Alice, age=30], User[name=Bob, age=41]]
```

**Listing 2.** The same captor accumulates: `getAllValues()` returned the value captured by the first `verify` plus both invocations matched by the second one.

Use a captor when the argument is a compound object and you want to assert on selected fields (`saved.name()`, `saved.age()`) with rich matchers from [[Which assertions does JUnit provide]] or AssertJ. For a single scalar argument, plain `verify(repo).save(new User("Alice", 30))` or an exact argument is simpler.

> [!warning] Captors are for verify, not for stubbing
> Mockito's own documentation recommends ArgumentCaptor with verification and against stubbing: a captor created in a `when(...)` chain reads worse, and if the stubbed call never happens, nothing is captured and the failure point moves away from the real defect. For stubbing with flexible matching, prefer argument matchers like `any()` or `argThat(...)`. Also note the accumulation trap in Listing 2 — reusing one captor across several `verify` calls makes `getAllValues()` contain duplicates from every matched invocation.

## Captor vs argThat

`verify(repo).save(argThat(u -> u.age() > 18))` answers "was it called with something valid?" inline. A captor answers "what exactly was passed?" and lets you fail with a rich message. If the matcher logic is reusable across tests, write an `ArgumentMatcher`; if it is a one-off field check, the captor keeps the test flatter. See [[How would you explain verify]] for how verification itself works, and [[What is the difference between Mock and MockBean]] for where a Mockito mock lives in a Spring test.

> [!tip] Interview answer
> **ArgumentCaptor captures the actual argument passed to a mock so you can assert on it after `verify`. You put `captor.capture()` in the verification call, then use `getValue()` for one call or `getAllValues()` for several. It is meant for verification, not stubbing, and one captor reused across verifies accumulates everything it matched.**

