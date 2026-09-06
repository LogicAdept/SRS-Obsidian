<!--
reps: 0
priority: 0
-->
#Java/StringJoiner #Java/Versions/8 #SRS

# How would you explain java.util.StringJoiner

> [!abstract] Short answer
> **`java.util.StringJoiner` (Java 8) builds a `String` of pieces separated by a delimiter, with an optional prefix and suffix.** `add` appends the next element and returns `this`. `toString` is `prefix + elements joined by delimiter + suffix`. While still empty (no `add`, no non-empty `merge`), that is `prefix + suffix`, or `setEmptyValue` if you set one. `Collectors.joining` is the stream form of the same idea. It is not `StringBuilder` and not SQL JOIN.

## Delimiter in the middle, brackets around the whole

Two constructors copy the given `CharSequence`s: delimiter only (no prefix/suffix), or delimiter + prefix + suffix. Any `null` delimiter, prefix, or suffix throws `NullPointerException`. The no-arg-prefix form’s empty `toString` is `""` unless `setEmptyValue` was used.

`add` copies the next element. `null` becomes the four characters `"null"`. After any `add`, the joiner is **not empty**, including `add("")`. `length()` equals `toString().length()`.

`merge(other)` appends **other’s contents without other’s prefix/suffix** as the next element if other is non-empty; a never-used other is a no-op. If other’s delimiter differs, those inner separators stay inside that **one** merged element. `merge(null)` throws `NullPointerException`.

`setEmptyValue` copies the fallback used only while empty. `null` emptyValue throws. Stream shortcut: `Collectors.joining(delimiter)` (and the prefix/suffix overload) ([[What is StringJoiner]], [[How would you explain java.lang.StringBuilder]]).

```d2
direction: down
sj: "StringJoiner\ndelimiter · prefix · suffix" {
  width: 280
  height: 50
}
add: "add(element)\nnull → \"null\"" {
  width: 240
  height: 45
}
out: "toString()\nprefix + joined + suffix" {
  width: 280
  height: 50
}
empty: "still empty?\nprefix+suffix or setEmptyValue" {
  width: 300
  height: 50
}

sj -> add
add -> out: "at least one add / non-empty merge"
sj -> empty: "no elements yet"
```

**Fig. 1.** Prefix and suffix wrap the whole result. The delimiter sits only **between** added elements.

```java
public class StringJoinerDemo {
    static String csv(String[] names) {
        StringJoiner sj = new StringJoiner(", ", "[", "]");
        for (String n : names) {
            sj.add(n);
        }
        return sj.toString(); // [a, b] or "[]" if names is empty
    }
}
```

**Listing 1.** Three-arg constructor is delimiter, prefix, suffix. An unused joiner’s `toString` is still `[]`, not `""`.

> [!warning] Empty is not “nothing”; `add(null)` is the word null
> Before any `add`, `toString` is `prefix + suffix` (for example `{}` with `"{"` / `"}"`), not `""`, unless you `setEmptyValue`. `add("")` makes it non-empty. `add(null)` inserts `"null"`. `merge` does not copy the other’s prefix/suffix. Constructor `null` delimiter/prefix/suffix → `NullPointerException`.

> [!tip] Interview answer
> **Java 8 helper: join pieces with a delimiter, optional prefix and suffix.** `add` then `toString`. Empty means `prefix+suffix` or `setEmptyValue`. Streams: `Collectors.joining`. Not a `StringBuilder`; `add(null)` becomes `"null"`.
