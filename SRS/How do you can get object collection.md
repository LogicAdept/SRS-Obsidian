<!--
reps: 0
priority: 0
-->
#Java/Collections #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Каким образом можно получить синхронизированные объекты стандартных коллекций?**

С помощью статических методов `synchronizedMap()` и `synchronizedList()` класса `Collections`. Данные методы возвращают синхронизированный декоратор переданной коллекции. При этом все равно в случае обхода по коллекции требуется ручная синхронизация.

```java
  Mindmap m = Collections.synchronizedMap(new HashMap());
  List l = Collections.synchronizedList(new ArrayList());
```

Начиная с Java 6 JCF был расширен специальными коллекциями, поддерживающими многопоточный доступ, такими как `CopyOnWriteArrayList` и `ConcurrentHashMap`.

**Как получить коллекцию только для чтения?**

При помощи:

+ `Collections.unmodifiableList(list)`;
+ `Collections.unmodifiableSet(set)`;
+ `Collections.unmodifiableMap(map)`.

Эти методы принимают коллекцию в качестве параметра, и возвращают коллекцию только для чтения с теми же элементами внутри.
