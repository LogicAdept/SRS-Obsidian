<!--
reps: 0
priority: 0
-->
#Java/Language #Java/Exceptions/TryCatch #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Можно ли в одном catch ловить несколько типов исключений?**

Да, multi-catch с Java 7: catch (IOException | SQLException e). Переменная при этом effectively final.

**Может ли один блок `catch` отлавливать сразу несколько исключений?**

В Java 7 стала доступна новая языковая конструкция, с помощью которой можно перехватывать несколько исключений одним блоком `catch`:

```java
try {
    //...
} catch(IOException | SQLException ex) {
    //...
}
```
