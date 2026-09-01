<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #Java/OOP/Constructors #SRS

> [!abstract] Short answer
> **Once per constant, during initialization of the enum class, in declaration order.** That initialization runs on first *active use* of the class — typically the first mention of a constant, or `values()` / `valueOf` — not on every later read, and not merely because the class file was loaded. You never call the constructor with `new`.

## Class initialization, not each later read

Each enum constant is an instance. The compiler turns it into a `public static final` field whose initializer creates that instance and passes any arguments after the name (`PENNY(1)`) into the constructor ([[Can you declare a constructor inside a Java enum]]). A constant is created when that field is initialized.

Those fields are initialized as part of initializing the enum class, in source order, **before** any extra `static` fields you write. First active use of the class is what starts that work: creating an instance, calling a `static` method declared on it, or reading a `static` field that is **not** a compile-time constant variable. Enum constants are objects, so `Coin.PENNY` is not a constant variable and **does** initialize the class. Loading the class without initializing it does not run constructors.

The constructor then runs **once for every constant**, including ones you have not named yet. `Coin.PENNY` still constructs `NICKEL`. After that, the instances are the only ones that will ever exist ([[Can you create a Java enum instance with new]], [[How does an enum provide a Singleton]]). A second `Coin.PENNY` is the same object; the constructor does not run again.

```d2
direction: down
use: "first active use\nCoin.PENNY or Coin.values()" {
  width: 300
  height: 60
  style.fill: "#e3f2fd"
}
init: "initialize Coin\nctor PENNY, then ctor NICKEL" {
  width: 300
  height: 60
  style.fill: "#e8f5e9"
}
later: "later reads reuse instances" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}

use -> init -> later
```

**Fig. 1.** One initialization of the enum class constructs the whole constant list.

```java
class Ctor {
    static int n;
}

enum Coin {
    PENNY(1), NICKEL(5);
    private final int cents;
    Coin(int cents) {
        this.cents = cents;
        Ctor.n++;
    }
    int cents() { return cents; }
}

class Demo {
    static int once() {
        int first = Coin.PENNY.cents();
        int again = Coin.PENNY.cents();
        return Ctor.n; // 2 — both constants, not once per read
        // first == 1, again == 1
    }
}
```

**Listing 1.** Naming `PENNY` still constructs `NICKEL`. The second read does not construct `PENNY` again.

> [!warning] “Class load” is not “constructor ran”
> Initialization is a distinct step from loading. `Class.forName(name, false, loader)` can load without initializing. The constructors run when the class is initialized.

> [!warning] A constant `int` on the enum does not construct the constants
> `static final int N = 1` is a constant variable. Using `Coin.N` need not initialize `Coin`, so constructors may not have run. `Coin.PENNY` always does. Do not treat enum constants as inlined compile-time ints ([[What is the advantage of a Java enum over int and String constant patterns]]).

> [!tip] Interview answer
> **The constructor runs once for each enum constant when the enum class is initialized — on first active use, in declaration order.** Touching one constant constructs them all. Later references reuse those instances; `new` is illegal. Arguments after a constant name (`PENNY(1)`) are the constructor arguments.
