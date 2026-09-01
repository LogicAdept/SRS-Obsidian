<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/String #Java/Arrays #SRS

# Why should arbitrary objects not be compared with double equals in Java?

> [!abstract] Short answer
> For two references, **`==` tests identity**: both `null`, or both the same object. It does not compare fields or characters. Distinct `String`s with the same text are `==` false; the language tells you to use `s.equals(t)`. Value types (`Integer`, your domain class, lists) override `equals` for content. `==` on those is a different, usually wrong, question.

## What `==` is specified to do

If both operands are reference types (or null), `==` is true when both are `null` or both refer to the **same** object or array; otherwise false. That is object equality in the language sense, not `equals`. It is a compile-time error when the types cannot be converted to each other by casting — those values could never be the same object (ignoring both-null).

```java
String s = new String("Ada");
String t = new String("Ada");
s == t;          // false: two objects
s.equals(t);     // true: same characters
```

**Listing 1.** The language’s own `String` warning. Interning or a literal pool may make two literals `==`; that is not a comparison strategy.

```d2
direction: down
q: "a == b  (references)" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
yes: "same object\nor both null" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
no: "two instances\neven with equal fields" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}

q -> yes
q -> no
```

**Fig. 1.** `==` never walks `equals`. Overriding `equals` does not change `==`.

## Why it bites

`Integer`, `List`, and a custom `Point` all override `equals`. `a == b` still means identity. Two `Integer` copies of `1000` may or may not be `==` depending on caching; that is irrelevant to value equality — use `equals` or `intValue`. Two arrays with the same elements are not `==`; use `Arrays.equals`.

Primitive `==` is a different operator: numeric / boolean equality. For `double`, it is **not** an equivalence relation (`NaN != NaN`, `+0.0 == -0.0`). `Double.equals` uses representation equivalence instead. Do not mix “I used `==` on the objects” with “I used `==` on the primitives inside `equals`.”

`HashMap` may use `==` as a **fast path** when the stored key is the same reference, then `equals`. Your client code should still pass a key that is `equals` to the stored one, not rely on `==`. [[How do you compare objects for equality in Java]] is the menu. [[How does Java decide whether two objects are equivalent]] is `equals` dispatch.

> [!warning] “It worked on String literals”
> `"Ada" == "Ada"` can be true because literals may share one interned object. `new String("Ada")` does not. Tests that use `==` on strings are accidental. Enum constants are a rare case where identity and equality coincide (`Enum.equals` is final and identity-based); that does not license `==` for arbitrary objects.

> [!tip] Interview answer
> **`==` on objects asks “same reference?”, not “same value?”. The JLS says even two `String`s with the same characters are `==` only if they are the same object; use `equals`. Wrappers, lists, and domain values override `equals` for content. `==` stays identity and will lie for copies.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Разница между == и equals() для строк.**

== сравнивает ссылки. equals() сравнивает содержимое. Для строк, созданных литералом, == может вернуть true из-за String Pool, но полагаться на это нельзя.

**Разница между == и equals() для строк.**

== сравнивает ссылки, equals() — содержимое. Для литералов == может дать true из-за String Pool, но полагаться на это нельзя.

**== vs equals для строк. Почему String immutable?**

== сравнивает ссылки (один объект в памяти?). equals — содержимое. String immutable: безопасность (ключи HashMap, передача в файлы/БД), потокобезопасность, кэширование hashCode, String Pool.

**== vs equals для строк?**

== сравнивает ссылки. equals — содержимое. Из-за String Pool два литерала "abc" == "abc" дадут true, но new String("abc") == "abc" — false (new создаёт новый объект вне пула). На собесе всегда отвечать «equals для содержимого».

**Разница между == и equals(). Что вернёт someObj.equals(null)?**

== сравнивает ссылки; equals(null) по контракту должен возвращать false.
