<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Language/Reflection/Class #SRS

# How do you inspect a Java record with reflection?

> [!abstract] Short answer
> Call `Class.isRecord()`, then `Class.getRecordComponents()`. That returns `RecordComponent[]` in **header order** (empty array if there are no components, **`null` if the class is not a record**). Each `RecordComponent` gives `getName()`, `getType()` / `getGenericType()`, and `getAccessor()` — invoke that `Method` on an instance to read the component. Added in Java 16, alongside records.

## Record-specific APIs, not `getDeclaredFields()`

```d2
direction: down
cls: "Class<?> c = obj.getClass()" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
check: "c.isRecord()" {
  width: 200
  height: 45
  style.fill: "#fff3e0"
}
comps: "c.getRecordComponents()\nheader order, never null if isRecord" {
  width: 340
  height: 70
  style.fill: "#e8f5e9"
}
rc: "name, type, generic type\naccessor Method, annotations" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
cls -> check
check -> comps
comps -> rc
```

**Fig. 1.** `isRecord` / `getRecordComponents` are the `Class` APIs that correspond to `isEnum` / enum constants. `java.lang.Record` itself is **not** a record class — `Record.class.isRecord()` is `false`.

JEP 395 and the Java SE records tutorial: `isRecord()` is true iff the class was declared as a record; `getRecordComponents()` returns one `java.lang.reflect.RecordComponent` per header component, in declaration order. `RecordComponent` (since 16) implements `AnnotatedElement` and exposes:

| Method | Role |
| --- | --- |
| `getName()` | component identifier |
| `getType()` | erased `Class` |
| `getGenericType()` | declared type including type arguments |
| `getAccessor()` | the public accessor `Method` |
| `getDeclaringRecord()` | the record `Class` |
| `getAnnotation` / `getAnnotations` | declaration annotations on the component |

Those accessors are the same mandated methods as [[What methods does the compiler generate for a Java record]]. `getDeclaredFields()` also sees the implicit `private final` component fields, but the array is **not ordered**, mixes in other declared fields (statics), and does not give you the accessor. See [[Where do annotations on Java record components apply]].

```java
if (!clazz.isRecord()) {
    throw new IllegalArgumentException("Not a record");
}
RecordComponent[] components = clazz.getRecordComponents();
for (RecordComponent rc : components) {
    String name = rc.getName();
    Class<?> type = rc.getType();
    Method accessor = rc.getAccessor();
    Object value = accessor.invoke(instance);
}
```

**Listing 1.** Guard with `isRecord()` so `getRecordComponents()` is non-null, then read each component through its accessor. An explicit accessor body runs here — [[Can you override a record accessor method]].

```java
static <T extends Record> Constructor<T> getCanonicalConstructor(Class<T> cls)
        throws NoSuchMethodException {
    Class<?>[] paramTypes = Arrays.stream(cls.getRecordComponents())
            .map(RecordComponent::getType)
            .toArray(Class<?>[]::new);
    return cls.getDeclaredConstructor(paramTypes);
}
```

**Listing 2.** Canonical constructor lookup from the `Class.getRecordComponents` API note: parameter types are the component types in header order.

A record with an empty header still has `isRecord() == true` and a **non-null empty** component array. The class-file picture matches the language: `final` class, superclass `java.lang.Record`, `private final` fields, canonical constructor, accessors — the same members `javap -p` prints. Generic components: use `getGenericType()`, not only `getType()` ([[Can a Java record be generic]]).

> [!warning] `getRecordComponents()` is `null` for non-records
> It is not an empty array. Skipping `isRecord()` and iterating the result throws `NullPointerException`. Arrays, ordinary classes, enums, and `java.lang.Record` all return `null` here.

> [!warning] `getDeclaredFields()` is not the record API
> Component fields exist, but their reflective order is unspecified and static fields sit in the same list. Header order, accessors, and component annotations live on `RecordComponent`.

> [!tip] Interview answer
> **Use `Class.isRecord()` and `Class.getRecordComponents()` — that is the record analogue of `isEnum()`, added in Java 16.** Each `RecordComponent` has name, type, and `getAccessor()`; invoke the accessor to read a value. Do not treat `getDeclaredFields()` as ordered components, and remember `getRecordComponents()` returns `null` when the class is not a record.
