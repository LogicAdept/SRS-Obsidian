<!--
reps: 0
priority: 0
-->
#Java/StringJoiner #Java/Versions/8 #SRS

# What is StringJoiner

> [!abstract] Short answer
> **`java.util.StringJoiner` (Java 8) builds a `String` of elements separated by a delimiter, with an optional prefix and suffix.** `add` appends the next piece; `toString` is `prefix + pieces joined by delimiter + suffix`. Empty (nothing added) is `prefix + suffix`, or a custom `setEmptyValue`. `Collectors.joining` uses the same idea on a stream. It is not `StringBuilder` and not SQL JOIN.

## Delimiter, then optional brackets

Two constructors copy the given `CharSequence`s: delimiter only (no prefix/suffix), or delimiter + prefix + suffix. All three in the three-arg form throw `NullPointerException` if any argument is `null`. `add` copies the next element and returns `this` for chaining. If the element is `null`, the characters `"null"` are added — the joiner is then non-empty even if you added `""` ([[How would you explain java.util.StringJoiner]], [[How would you explain java.lang.String]]).

`toString` is prefix, then added values separated by the delimiter, then suffix. Before any `add` (and with no non-empty `merge`), that is `prefix + suffix`, unless `setEmptyValue` was called. `length()` matches `toString().length()`. `merge(other)` appends **other’s contents without other’s prefix/suffix** as the next element if other is non-empty; other’s delimiter stays inside that one element if it differs ([[What is the difference between StringBuilder and StringBuffer]], [[How would you explain the StringBuilder append method]]).

The class javadoc shows `Collectors.joining(CharSequence)` (and the prefix/suffix overload) as the stream form of the same pattern.

```d2
sj: "StringJoiner\ndelimiter · prefix · suffix" {
  shape: rectangle
}
add: "add(element)\nnull → \"null\"" {
  shape: rectangle
}
out: "toString()\nprefix + joined + suffix" {
  shape: rectangle
}
empty: "still empty?\nprefix+suffix\nor setEmptyValue" {
  shape: rectangle
}
sj -> add
add -> out: "at least one add/merge"
sj -> empty: "no elements yet"
```

**Fig. 1.** Prefix and suffix wrap the whole result. The delimiter sits only **between** added elements.

```java
StringJoiner sj = new StringJoiner(":", "[", "]");
sj.add("George").add("Sally").add("Fred");
String desiredString = sj.toString(); // [George:Sally:Fred]

StringJoiner withEnds = new StringJoiner(".", "prefix-", "-suffix");
for (String s : "Hello the brave world".split(" ")) {
    withEnds.add(s);
}
System.out.println(withEnds); // prefix-Hello.the.brave.world-suffix
```

**Listing 1.** Three-arg constructor is delimiter, prefix, suffix. First block matches the Java 8 `StringJoiner` API note; second is the dump example, which prints the same way.

> [!warning] Empty is not “nothing”; `add(null)` is the word null
>
> An unused joiner’s `toString` is still `prefix + suffix` (e.g. `{}` for `"{"`, `"}"`), not `""`, unless you `setEmptyValue`. After any `add`, it is no longer empty — including `add("")`. `add(null)` inserts `"null"`. `merge` does not copy the other’s prefix/suffix. Constructor `null` delimiter/prefix/suffix → `NullPointerException`.

> [!tip] Interview answer
>
> **Java 8 `final` class: join pieces with a delimiter, optional prefix and suffix.** `add` / `toString`. Empty → `prefix+suffix` or `setEmptyValue`. Stream shortcut: `Collectors.joining`. Not a `StringBuilder`; `add(null)` becomes `"null"`.
