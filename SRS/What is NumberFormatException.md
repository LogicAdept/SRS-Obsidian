<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Language/Wrappers #SRS

# What is `NumberFormatException`?

> [!abstract] Short answer
> **An unchecked `RuntimeException` when a string cannot be converted to a number because the text is not in the right format.** `Integer.parseInt("abc")` is the usual example. It also fires for overflow of the target type (`parseInt("2147483648")`).

## Bad text for a numeric parse, under `IllegalArgumentException`

`NumberFormatException` extends `IllegalArgumentException`, hence `RuntimeException`. You do not declare it in `throws`. `catch (IllegalArgumentException e)` **does** catch a parse failure ([[Is RuntimeException a subclass of Exception]], [[Must you declare RuntimeException in a throws clause]], [[Should you throw NullPointerException or IllegalArgumentException for a null argument]], [[What is the difference between IllegalArgumentException and IllegalStateException]]).

`Integer.parseInt(String)` returns `int` and throws `NumberFormatException` if the string is not a parsable integer. `Integer.valueOf(String)` parses the same way, then boxes; it throws the **same** type on bad text. The difference is the return type (`int` vs `Integer`), not the exception. The same pattern exists on `Long`, `Double`, and the other wrappers.

Interview lists put it next to `NullPointerException` and `ArithmeticException` as a common unchecked type. It is not integer divide-by-zero and not a null dereference ([[What is ArithmeticException]], [[What is NullPointerException]], [[What are common kinds of unchecked exceptions in Java]]).

The `CharSequence` `parseInt` overload throws `NullPointerException` if the sequence is `null`. The `String` overload documents `NumberFormatException` when the string is not parsable.

```d2
direction: down
rte: RuntimeException {
  width: 240
  height: 40
}
iae: IllegalArgumentException {
  width: 260
  height: 40
  style.fill: "#fff8e1"
}
nfe: NumberFormatException {
  width: 260
  height: 40
  style.fill: "#ffebee"
}
parse: "Integer.parseInt(\"abc\")" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
rte -> iae
iae -> nfe
parse -> nfe
```

**Fig. 1.** Parse failures are `NumberFormatException`, which is an `IllegalArgumentException`.

```java
class Demo {
    static int parseBad() {
        return Integer.parseInt("abc");
    }

    static Integer valueOfBad() {
        return Integer.valueOf("abc");
    }

    static int tooBig() {
        return Integer.parseInt("2147483648");
    }
}
```

**Listing 1.** All three throw `NumberFormatException` at run time. `parseBad` and `valueOfBad` fail on format; `tooBig` fails because the value does not fit in `int`. You may catch it like any unchecked exception ([[Can you catch an unchecked exception in Java]]). None of these methods needs `throws`.

> [!warning] `catch (IllegalArgumentException)` swallows parse failures
> Because `NumberFormatException` is a subclass, a handler written for “bad arguments” also catches `parseInt`. That is easy to miss in a review.

> [!warning] `parseInt` vs `valueOf` is the return type, not the exception
> Both throw `NumberFormatException` on `"abc"`. `parseInt` yields `int`. `valueOf` yields `Integer`. Do not invent a second exception name for boxing.

> [!tip] Interview answer
> **`NumberFormatException` is an unchecked exception when a string is not a valid number for that parse** — `Integer.parseInt("abc")`, or a value that does not fit. It extends `IllegalArgumentException`, so `catch (IllegalArgumentException)` matches it. `parseInt` and `valueOf` throw the same type; they differ only in `int` versus `Integer`.
