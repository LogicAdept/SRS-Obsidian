<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Предположим, есть метод, который может выбросить `IOException` и `FileNotFoundException` в какой последовательности должны идти блоки `catch`? Сколько блоков `catch` будет выполнено?**

Общее правило: обрабатывать исключения нужно от «младшего» к старшему. Т.е. нельзя поставить в первый блок `catch(Exception ex) {}`, иначе все дальнейшие блоки `catch()` уже ничего не смогут обработать, т.к. любое исключение будет соответствовать обработчику `catch(Exception ex)`.

Таким образом, исходя из факта, что `FileNotFoundException extends IOException` сначала нужно обработать `FileNotFoundException`, а затем уже `IOException`:

```java
void method() {
    try {
        //...
    } catch (FileNotFoundException ex) {
        //...
    } catch (IOException ex) {
        //...
    }
}
```
