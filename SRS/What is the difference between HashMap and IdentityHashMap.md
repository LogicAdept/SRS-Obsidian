<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/IdentityHashMap #Java/HashCodeEquals #SRS

# What is the difference between `HashMap` and `IdentityHashMap`?

> [!abstract] Short answer
> `HashMap` compares keys with **`equals`** (after `hashCode`). `IdentityHashMap` compares keys **and values** with **`==`** and hashes with **`System.identityHashCode`**. It implements `Map` but **intentionally violates** the `Map` contract that equality is `equals`. Use it only when you must distinguish references that would be `equals`. `HashMap` is the general-purpose map.

## Equality and hashing

```text
HashMap
  k1 and k2 same key iff  (k1==null ? k2==null : k1.equals(k2))
  bucket from key.hashCode() (then mixed)

IdentityHashMap
  k1 and k2 same key iff  (k1==k2)
  bucket from System.identityHashCode(key)
```

**Listing 1.** Documented key tests. `IdentityHashMap` also uses reference equality for values in `containsValue` / entry equality.

Two `String` copies with the same characters are one `HashMap` key and two `IdentityHashMap` keys. Overriding `equals`/`hashCode` on your class does **not** change `IdentityHashMap`. `System.identityHashCode` still reports the default hash after an override. [[How are hashCode and equals implemented in java.lang.Object]] is that default.

The class javadoc states it is **not** a general-purpose `Map`: `Map` mandates `equals`. Typical uses are a node table for serialization or deep copy (must not merge distinct objects that happen to be `equals`) and proxy tables. [[What is IdentityHashMap for]] is that niche.

```d2
direction: down
k: "Two instances\nequals true, != references" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
hm: "HashMap\none mapping" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
ihm: "IdentityHashMap\ntwo mappings" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}

k -> hm
k -> ihm
```

**Fig. 1.** Same value, different references: `HashMap` coalesces, `IdentityHashMap` does not.

## Structure and tuning

`HashMap` is a bucket table with chaining and, in Java 8+, optional tree bins. You tune **initial capacity** and **load factor** (default 0.75). Iteration is proportional to capacity plus size.

An **implementation note** (not the `Map` contract) describes `IdentityHashMap` as a **linear-probe** table: one array of alternating keys and values. You tune **expected maximum size** (default 21), not a load factor. Iteration is proportional to the number of buckets. Both allow `null` keys and values; neither is synchronized; neither promises iteration order.

Constant-time `get`/`put` is assumed when hashes disperse: user `hashCode` for `HashMap`, identity hash for `IdentityHashMap`. [[Does HashMap guarantee its documented lookup time complexity]] is that assumption on the `equals` map.

Entry `hashCode` in `IdentityHashMap` is `identityHashCode(key) XOR identityHashCode(value)`, matching its `==` entry equality. `HashMap` entries use `Objects.hashCode` on key and value.

> [!warning] Do not swap them for “speed”
> The implementation note that linear probing can be faster for some mixes is not a license to drop `equals`. If you need value keys, `HashMap` is the contract you want. If you need reference keys, `IdentityHashMap` is the rare tool. Putting value objects into `IdentityHashMap` and expecting `get(new Key(id))` to hit is the usual bug.

> [!tip] Interview answer
> **`HashMap` is value equality: `hashCode` then `equals`. `IdentityHashMap` is reference equality: `==` and `identityHashCode`, and it admits it violates the `Map` contract. Use the first by default. Use the second for identity-sensitive tables (graph copy, proxies). Both allow null; they differ in comparison, hashing, and table shape (chains versus linear probe).**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В чем разница между `HashMap` и `IdentityHashMap`? Для чего нужна `IdentityHashMap`?**

`IdentityHashMap` - это структура данных, так же реализующая интерфейс `Mindmap` и использующая при сравнении ключей (значений) сравнение ссылок, а не вызов метода `equals()`. Другими словами, в `IdentityHashMap` два ключа `k1` и `k2` будут считаться равными, если они указывают на один объект, т.е. выполняется условие `k1` == `k2`.

`IdentityHashMap` не использует метод `hashCode()`, вместо которого применяется метод `System.identityHashCode()`, по этой причине `IdentityHashMap` по сравнению с `HashMap` имеет более высокую производительность, особенно если последний хранит объекты с дорогостоящими методами `equals()` и `hashCode()`.

Одним из основных требований к использованию `HashMap` является неизменяемость ключа, а, т.к. `IdentityHashMap` не использует методы  `equals()` и `hashCode()`, то это правило на него не распространяется.

`IdentityHashMap` может применяться для реализации сериализации/клонирования. При выполнении подобных алгоритмов программе необходимо обслуживать хэш-таблицу со всеми ссылками на объекты, которые уже были обработаны. Такая структура не должна рассматривать уникальные объекты как равные, даже если метод `equals()` возвращает `true`.

Пример кода:
```java
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.Mindmap;

public class Q2 {

    public static void main(String[] args) {
        Q2 q = new Q2();
        q.testHashMapAndIdentityHashMap();
    }

    private void testHashMapAndIdentityHashMap() {
        CreditCard visa = new CreditCard("VISA", "04/12/2019");

        Mindmap<CreditCard, String> cardToExpiry = new HashMap<>();
        Mindmap<CreditCard, String> cardToExpiryIdenity = new IdentityHashMap<>();

        System.out.println("adding to HM");
        // inserting objects to HashMap
        cardToExpiry.put(visa, visa.getExpiryDate());

        // inserting objects to IdentityHashMap
        cardToExpiryIdenity.put(visa, visa.getExpiryDate());
        System.out.println("adding to IHM");

        System.out.println("before modifying keys");
        String result = cardToExpiry.get(visa) != null ? "Yes" : "No";
        System.out.println("Does VISA card exists in HashMap? " + result);

        result = cardToExpiryIdenity.get(visa) != null ? "Yes" : "No";
        System.out.println("Does VISA card exists in IdenityHashMap? " + result);

        // modifying value object
        visa.setExpiryDate("02/11/2030");

        System.out.println("after modifying keys");
        result = cardToExpiry.get(visa) != null ? "Yes" : "No";
        System.out.println("Does VISA card exists in HashMap? " + result);

        result = cardToExpiryIdenity.get(visa) != null ? "Yes" : "No";
        System.out.println("Does VISA card exists in IdenityHashMap? " + result);

        System.out.println("cardToExpiry.containsKey");
        System.out.println(cardToExpiry.containsKey(visa));
        System.out.println("cardToExpiryIdenity.containsKey");
        System.out.println(cardToExpiryIdenity.containsKey(visa));
    }

}

class CreditCard {
    private String issuer;
    private String expiryDate;

    public CreditCard(String issuer, String expiryDate) {
        this.issuer = issuer;
        this.expiryDate = expiryDate;
    }

    public String getIssuer() {
        return issuer;
    }

    public String getExpiryDate() {
        return expiryDate;
    }

    public void setExpiryDate(String expiry) {
        this.expiryDate = expiry;
    }

    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((expiryDate == null) ? 0 : expiryDate.hashCode());
        result = prime * result + ((issuer == null) ? 0 : issuer.hashCode());
        System.out.println("hashCode = " + result);
        return result;
    }

    @Override
    public boolean equals(Object obj) {
        System.out.println("equals !!! ");
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        CreditCard other = (CreditCard) obj;
        if (expiryDate == null) {
            if (other.expiryDate != null)
                return false;
        } else if (!expiryDate.equals(other.expiryDate))
            return false;
        if (issuer == null) {
            if (other.issuer != null)
                return false;
        } else if (!issuer.equals(other.issuer))
            return false;
        return true;
    }

}
```

Результат выполнения кода:
```
adding to HM
hashCode = 1285631513
adding to IHM
before modifying keys
hashCode = 1285631513
Does VISA card exists in HashMap? Yes
Does VISA card exists in IdenityHashMap? Yes
after modifying keys
hashCode = 791156485
Does VISA card exists in HashMap? No
Does VISA card exists in IdenityHashMap? Yes
cardToExpiry.containsKey
hashCode = 791156485
false
cardToExpiryIdenity.containsKey
true
```
