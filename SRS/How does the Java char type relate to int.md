<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`char` is a 16-bit unsigned integer holding a single UTF-16 code unit. Because it is numeric, it participates in arithmetic and auto-promotes to `int`.

```java
char c = 'A';
int code = c;            // 65 (implicit widening)
char next = (char) (c + 1); // 'B' (must cast back, since c+1 is int)
System.out.println('a' + 'b'); // 195, not "ab" — numeric addition!
```

A frequent gotcha: `'a' + 'b'` adds the code points, while `"" + 'a' + 'b'` concatenates. Characters beyond the Basic Multilingual Plane (emoji) need two chars (a surrogate pair) or `int` code points.

> [!warning] Unverified traps from the dump
> - `char + char` is numeric `int` addition, not string concatenation.
> - Assigning `c + 1` back to `char` needs a cast.
