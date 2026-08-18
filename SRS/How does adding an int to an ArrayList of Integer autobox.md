<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Collections #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

When elements are added with `add()` and the list is `List<Integer>`, dumps say the compiler automatically treats `list.add(i)` as `add(Integer.valueOf(i))`. Autoboxing is the name for that primitive-to-wrapper conversion.

```java
List<Integer> list = new ArrayList<>();
for (int i = 0; i < 10; i++) {
    list.add(i); // Integer.valueOf(i)
}
int num = list.get(0); // unboxing
```

> [!warning] Unverified traps from the dump
> - Each `add` of a primitive may allocate or reuse a cached `Integer`.
> - Reading with `int n = list.get(k)` unboxes and NPEs if the element is `null`.
