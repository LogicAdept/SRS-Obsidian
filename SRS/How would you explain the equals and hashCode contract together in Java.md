<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals/Contract #SRS

# How would you explain the `equals` and `hashCode` contract together in Java?

> [!abstract] Short answer
> `equals` defines **logical equality**; `hashCode` provides a hash value that hash-based collections use to narrow their search. Their key relationship is one-way: if `a.equals(b)` is `true`, then `a.hashCode()` and `b.hashCode()` **must** be equal. Equal hash codes do not imply equal objects. Therefore, whenever a class gives `equals` value semantics, its `hashCode` must be compatible with those same semantics.

## The two contracts

### What `equals` must guarantee

For non-null references, `equals` defines an equivalence relation:

- **Reflexive:** `x.equals(x)` is `true`.
- **Symmetric:** `x.equals(y)` has the same result as `y.equals(x)`.
- **Transitive:** if `x` equals `y` and `y` equals `z`, then `x` equals `z`.
- **Consistent:** repeated calls return the same result while equality-relevant state is unchanged.
- **Non-null:** `x.equals(null)` is `false`.

The implementation inherited from `Object` uses reference identity: two references are equal only when they refer to the same object. Override it when distinct instances should represent the same logical value. See [[What is the Object equals contract]].

### What `hashCode` must guarantee

- Repeated calls on one object return the same integer during an application execution while equality-relevant state is unchanged.
- Objects that are equal according to `equals` return the same hash code.
- Unequal objects may return the same hash code; collisions are legal.
- A hash code need not remain the same across different application executions.

The contract does **not** require unique hashes, and `hashCode` does not prove equality. Its purpose is to partition candidates efficiently before an equality check. See [[How would you explain the hashCode method contract in Java]].

> [!warning] The implication is one-way
> `a.equals(b) == true` requires equal hash codes. The inverse is false: equal hash codes may belong to unequal objects. A constant `hashCode` is contract-correct but performs poorly because every key collides. [[When does a hashCode collision occur in a HashMap]] explains that case.

## How `HashMap` uses the relationship

```d2
direction: down
equal: "a.equals(b) == true" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
required: "Required:\na.hashCode() == b.hashCode()" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
candidate: "Same HashMap spread hash\nand candidate bin" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
verify: "HashMap still checks\nidentity or equals" {
  width: 280
  height: 85
  style.fill: "#e8f5e9"
}
collision: "Same hash alone\nmay describe unequal keys" {
  width: 280
  height: 85
  style.fill: "#fff3e0"
}

equal -> required
required -> candidate
candidate -> verify
required -> collision: inverse does not follow
```

**Fig. 1.** Equality requires the same hash and therefore the same candidate bin in one `HashMap`. A matching hash only selects candidates; identity or `equals` still decides whether a key matches.

In OpenJDK `HashMap`, lookup first compares a node's stored hash with the lookup hash. Only after the hashes match does it test key identity and then `equals`. If two logically equal keys return different hashes, they can be stored as separate mappings because the equality check may never run. This is why [[Why should equals and hashCode be overridden together]] is a correctness rule, not merely a performance recommendation.

## A correct immutable value key

```java
import java.util.HashMap;
import java.util.Map;

public class Main {
    static final class UserId {
        private final long value;

        UserId(long value) {
            this.value = value;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof UserId)) return false;
            UserId other = (UserId) o;
            return value == other.value;
        }

        @Override
        public int hashCode() {
            return Long.hashCode(value);
        }
    }

    public static void main(String[] args) {
        UserId first = new UserId(42);
        UserId second = new UserId(42);

        Map<UserId, String> users = new HashMap<>();
        users.put(first, "Alice");

        System.out.println(first.equals(second));                // true
        System.out.println(first.hashCode() == second.hashCode()); // true
        System.out.println(users.get(second));                   // Alice
    }
}
```

**Listing 1.** Java 8+ value semantics for an immutable key. The class is `final`, `equals` compares `value`, and `hashCode` derives from the same value; an equal, distinct instance retrieves the existing mapping.

The hash implementation may use fewer fields than `equals` and still satisfy the contract—even a constant is legal—but using the same stable identity fields usually gives better distribution. It must not include a field that `equals` ignores if equal objects may differ in that field, because those equal objects could then receive different hashes.

> [!warning] Common implementation failures
> - Overriding `equals` without a compatible `hashCode`, which can violate the required implication. Overriding only `hashCode` is usually unnecessary, but it is not automatically a contract violation while `equals` retains identity semantics and the returned hash remains stable.
> - Using mutable fields and changing them while the object is stored in a hash-based collection; see [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]].
> - Using `instanceof` in an extensible base class while a subclass adds equality state, which can break symmetry. A final value class avoids that inheritance problem; non-final hierarchies need an explicit equality design.

> [!tip] Interview answer
> **`equals` defines logical equality, while `hashCode` lets hash-based collections narrow the candidate set. If two objects are equal, they must have the same hash code, but the same hash does not mean they are equal. Therefore, override both methods consistently, base them on stable logical identity, and remember that collisions between unequal objects are valid.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Контракт equals/hashCode.**

Если a.equals(b) == true, то a.hashCode() == b.hashCode(). Обратное необязательно (коллизии допустимы). equals(null) → false. Переопределяешь один — переопределяй оба. Практический пример: положить объект в HashSet, изменить поле в hashCode — объект потеряется, contains() вернёт false.

**Контракт equals/hashCode.**

1) Если a.equals(b), то a.hashCode() == b.hashCode(). 2) Если хэшкоды разные — объекты точно не равны. Если переопределяешь один — переопределяй и второй.

**Контракт equals/hashCode.**

Если a.equals(b), то a.hashCode() == b.hashCode(). Обратное не обязательно. Переопределяешь один — переопределяй и второй.

**Расскажи контракт equals и hashCode.**

Контракт equals: рефлексивность (a.equals(a) = true), симметричность (a.equals(b) ⇔ b.equals(a)), транзитивность (a=b и b=c → a=c), консистентность (повторный вызов даёт тот же результат), equals(null) = false. Главное правило связки: если a.equals(b), то a.hashCode() == b.hashCode(). Обратное не обязано выполняться.

**Контракт equals/hashCode. Что сломается при нарушении?**

Если a.equals(b), то hashCode совпадают. Иначе HashMap/HashSet теряют объекты.

**Расскажите про контракт equals/hashCode. Что случится с HashMap при константном hashCode?**

Если a.equals(b), то hashCode одинаков. Обратное необязательно. При константном hashCode — все в одном bucket: Java 7 — список O(n), Java 8+ при 8 коллизиях — red-black tree O(log n). Деградация. При рандомном — объект «потеряется» при get().

**Контракт equals/hashCode.**

a.equals(b) → hashCode одинаков. Обратное необязательно. Переопределяешь один — переопределяй оба. Нарушение ломает HashMap/HashSet: объект «теряется» при изменении поля в hashCode.

**Контракт equals/hashCode.**

Если a.equals(b), то hashCode одинаков. Обратное необязательно. Рефлексивность, симметричность, транзитивность. equals(null) → false. Переопределяешь один — переопределяй оба. Нарушение ломает HashMap/HashSet.
