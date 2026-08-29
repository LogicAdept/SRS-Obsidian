<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #Java/IO #SRS

# In what order should catch blocks appear for `IOException` and `FileNotFoundException`?

> [!abstract] Short answer
> **`FileNotFoundException` first, then `IOException`.** `FileNotFoundException` extends `IOException`. The first matching `catch` wins. Catching the superclass first makes the subclass clause **unreachable** — that is a compile-time error, not a warning you can ignore.

## Specific type, then the wider I/O net

`FileNotFoundException` is a subclass of `IOException`. A `throw` of the subclass is assignment-compatible with `catch (IOException)`. The `try` statement uses the **leftmost** matching clause ([[How many catch blocks execute for one thrown exception]], [[Does throws IOException cover FileNotFoundException]]).

If `catch (IOException)` appears **above** `catch (FileNotFoundException)`, the second clause can catch a type the first already catches. That is a compile-time error.

Put the subclass first when you need different handling (missing file vs other I/O). If both should do the same work, catch only `IOException` — or do not list both in one multi-`catch`: alternatives must not be related that way ([[Can one catch block handle multiple exception types in Java]]).

`throws IOException` still covers throwing `FileNotFoundException`. Catch order is the opposite instinct: **narrow handler before wide**.

```d2
direction: down
throw: "FileNotFoundException" {
  width: 300
  height: 50
}
fnf: "catch (FileNotFoundException)" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}
ioe: "catch (IOException)" {
  width: 280
  height: 50
}
throw -> fnf -> ioe
```

**Fig. 1.** Subclass clause first. The `IOException` clause is for other I/O types only.

```java
class Demo {
    static void read() {
        try {
            throw new java.io.FileNotFoundException("missing");
        } catch (java.io.FileNotFoundException e) {
            System.out.println("missing");
        } catch (java.io.IOException e) {
            System.out.println("other I/O");
        }
    }
}
```

**Listing 1.** Legal order. Swap the two `catch` clauses and the program does not compile.

> [!warning] Superclass first does not “fall through”
> Java will not try the next `catch` of the same `try`. The compiler rejects the dead `FileNotFoundException` clause.

> [!warning] `catch (IOException | FileNotFoundException e)` is illegal
> Multi-`catch` alternatives cannot be a subclass of one another. Use one type, or two ordered clauses.

> [!tip] Interview answer
> **Catch `FileNotFoundException` before `IOException` because the subclass is a kind of `IOException`.** The first matching `catch` is the only one that runs. Reverse the order and the compiler reports that `FileNotFoundException` is already caught.
