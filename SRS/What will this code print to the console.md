<!--
reps: 0
priority: 0
-->
#Java/OOP/Initialization #Career/Interview/Exercises #SRS

# What will this code print to the console?

> [!abstract] Short answer
> **Seven lines:** `a`, `b`, `c`, `2`, `3`, `4`, `1`. Class init runs **`s1` then `static { }` then `s2`** (textual static order). `new Test()` then runs instance **`s3`, `{ }`, `s4`**, then the **constructor body**. The constructor is written at the top of the file; it still runs **last**. Hierarchy order: [[What is the order of constructors and initializer blocks in a class hierarchy]]. Statics: [[How would you explain static initialization order in Java]]. `{ }` vs ctor: [[How would you explain instance initializer blocks versus constructors]].

## Trace `main` → class init → `new`

`main` does `new Test()`. That **initializes class `Test`**, then **constructs** one instance ([[What is constructor]]; [[What is constructor]]).

**Static sequence (once), source order of static field initializers and `static { }` only:**

1. `static String s1 = sP1("a")` → prints `a`  
2. `static { s1 = sP1("b"); }` → prints `b`  
3. `static String s2 = sP1("c")` → prints `c`  

The constructor declaration and instance `{ }` do **not** participate here. `sP1` is a `static` method; calling it from static init is fine.

**Instance sequence** after `super()` (`Object()`), source order of instance field initializers and `{ }`, then the constructor epilogue ([[How would you explain static and instance initializer blocks in Java]]):

4. `String s3 = sP1("2")` → `2`  
5. `{ s1 = sP1("3"); }` → `3`  
6. `String s4 = sP1("4")` → `4`  
7. constructor body `s1 = sP1("1")` → `1`  

Each `println` is its own line. The dump’s `a b c 2 3 4 1` is the **tokens**, not a single spaced line.

```d2
direction: down
st: "a → b → c\nclass init" {
  width: 180
  height: 45
  style.fill: "#e3f2fd"
}
in: "2 → 3 → 4 → 1\ninstance + ctor" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
st -> in: "new Test()"
```

**Fig. 1.** Statics of `Test`, then this instance. Constructor body is after `{ }` and field initializers.

```java
public class Test {
    public Test() {
        s1 = sP1("1");
    }

    static String s1 = sP1("a");

    String s3 = sP1("2");

    {
        s1 = sP1("3");
    }

    static {
        s1 = sP1("b");
    }

    static String s2 = sP1("c");

    public static void main(String[] args) {
        Test ft = new Test();
    }

    private static String sP1(String s) {
        System.out.println(s);
        return s;
    }

    String s4 = sP1("4");
}
```

**Listing 1.** Same program as the prompt. Console:

```
a
b
c
2
3
4
1
```

> [!warning] Where the constructor sits in the file does not change when it runs
> `Test()` is parsed first, executed last for this `new`. Instance `{ }` and field initializers of this class run after `super()`, before the constructor’s assignments.

> [!warning] Mix static and instance when reading top to bottom
> A human scanning the file sees ctor, `s1`, `s3`, `{ }`, `static`, `s2`, `s4`. The VM splits **static** vs **instance** sequences. `s3` is not static and does not run during class init.

> [!warning] `s1` is overwritten several times
> After the program, `s1` is `"1"`. Nothing prints the field; only `sP1`’s argument is printed. `ft` is unused besides construction.

> [!tip] Interview answer
> Print each `sP1` argument as class initialization and then construction run. Statics in textual order: a, b, c. Then instance initializers in textual order: 2, 3, 4. Then the constructor body: 1. Seven lines, not one. The constructor at the top of the class is not the first code that runs.
