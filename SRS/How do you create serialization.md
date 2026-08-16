<!--
reps: 0
priority: 0
-->
#Java/Serialization #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как создать собственный протокол сериализации?**

Для создания собственного протокола сериализации достаточно реализовать интерфейс `Externalizable`, который содержит два метода:

```java
public void writeExternal(ObjectOutput out) throws IOException;
public void readExternal(ObjectInput in) throws IOException, ClassNotFoundException;
```
