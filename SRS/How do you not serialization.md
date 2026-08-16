<!--
reps: 0
priority: 0
-->
#Java/Serialization #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как не допустить сериализацию?**

Чтобы не допустить автоматическую сериализацию можно переопределить `private` методы для создания исключительной ситуации `NotSerializableException`.

```java
private void writeObject(ObjectOutputStream out) throws IOException {
    throw new NotSerializableException();
}

private void readObject(ObjectInputStream in) throws IOException {
    throw new NotSerializableException();
}
```

Любая попытка записать или прочитать этот объект теперь приведет к возникновению исключительной ситуации.
