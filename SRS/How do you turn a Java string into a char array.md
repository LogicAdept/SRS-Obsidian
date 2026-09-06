<!--
reps: 0
priority: 0
-->
#Java/String #SRS

# How do you turn a Java string into a char array

> [!abstract] Short answer
> **Call `toCharArray()`.** It returns a **newly allocated** `char[]` whose length is `s.length()` and whose contents are the string’s UTF-16 `char` sequence. That array is a **copy**: mutating it does not change the `String`. To copy a **range** into a buffer you already own, use `getChars(srcBegin, srcEnd, dst, dstBegin)` (end exclusive). `charAt` is one code unit; `chars()` / `codePoints()` are streams, not arrays.

## Copy of UTF-16 code units

A `String` is an immutable UTF-16 sequence. Indexes count **`char` code units**. A supplementary character is a **surrogate pair** and occupies **two** slots in both the string and the array from `toCharArray()`.

`toCharArray()` is the whole-string conversion: new array, length equals `length()`, filled with that sequence. The method contract is a **new** array, not a handle to any internal field ([[Is it accurate to say String is backed by a character array internally]]).

`getChars` copies `srcEnd - srcBegin` characters from the string into `dst` starting at `dstBegin`. Bounds that throw `IndexOutOfBoundsException`: `srcBegin < 0`, `srcBegin > srcEnd`, `srcEnd > length()`, `dstBegin < 0`, or `dstBegin + (srcEnd - srcBegin) > dst.length`. A `null` `dst` throws `NullPointerException` (class-wide rule for `null` arguments).

The reverse copy is `new String(char[])` / `new String(char[], offset, count)`: the constructor **copies** the array, so later writes to it do not change the `String`. For passwords, the useful property is that **you** can wipe the `char[]` after use; you cannot wipe a `String` ([[Why is a char array preferred over String for passwords]]).

```d2
direction: down
s: "String (immutable UTF-16)" {
  width: 260
  height: 45
}
full: "toCharArray()\nnew char[length]" {
  width: 240
  height: 50
}
range: "getChars(begin, end, dst, off)\ninto caller buffer" {
  width: 280
  height: 50
}
stream: "chars() / codePoints()\nIntStream, not char[]" {
  width: 260
  height: 50
}

s -> full: "whole copy"
s -> range: "slice copy"
s -> stream: "not an array"
```

**Fig. 1.** The array APIs copy code units. Streams are a different shape; they do not replace `toCharArray()`.

```java
public class ToCharArrayDemo {
    static void demo(String s) {
        char[] copy = s.toCharArray(); // length == s.length(); independent of s
        if (s.isEmpty()) {
            return;
        }
        copy[0] = 'x';
        s.charAt(0); // still the original first char

        char[] buf = new char[s.length() + 1];
        s.getChars(0, s.length(), buf, 1); // dst[1 .. length]
    }
}
```

**Listing 1.** `toCharArray()` allocates. `getChars` writes into an existing array. Mutating either array does not mutate `s`.

> [!warning] Copy, surrogates, and the wrong API
> The result is **not** a live view of the string. One emoji or other supplementary character is **two** `char`s — `toCharArray().length` is `length()`, not the code-point count (`codePoints()` if you need scalars). `getBytes(...)` encodes to `byte[]` and is not a char array. `getChars` does not allocate: a short `dst` or a bad range is `IndexOutOfBoundsException`, not a silent truncate.

> [!tip] Interview answer
> **`s.toCharArray()` — a new `char[]` copy of the UTF-16 units, same length as the string.** Changing the array does not change `s`. Use `getChars` to fill a buffer you already have. Surrogate pairs take two slots; `getBytes` is a different conversion.
