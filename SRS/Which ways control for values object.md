<!--
reps: 0
priority: 0
-->
#Java/Serialization #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие существуют способы контроля за значениями десериализованного объекта**

Если есть необходимость выполнения контроля за значениями десериализованного объекта, то можно использовать интерфейс `ObjectInputValidation` с переопределением метода `validateObject()`.

```java
// Если вызвать метод validateObject() после десериализации объекта, то будет вызвано исключение InvalidObjectException при значении возраста за пределами 39...60.
public class Person implements java.io.Serializable,
                               java.io.ObjectInputValidation {
    ...
    @Override
    public void validateObject() throws InvalidObjectException {
        if ((age < 39) || (age > 60))
            throw new InvalidObjectException("Invalid age");
    }
}
```

Так же существуют способы подписывания и шифрования, позволяющие убедиться, что данные не были изменены:

+ с помощью описания логики в `writeObject()` и `readObject()`.

+ поместить в оберточный класс `javax.crypto.SealedObject` и/или `java.security.SignedObject`. Данные классы являются сериализуемыми, поэтому при оборачивании объекта в `SealedObject` создается подобие «подарочной упаковки» вокруг исходного объекта. Для шифрования необходимо создать симметричный ключ, управление которым должно осуществляться отдельно. Аналогично, для проверки данных можно использовать класс `SignedObject`, для работы с которым также нужен симметричный ключ, управляемый отдельно.

# Источники
+ [IBM developerWorks](https://www.ibm.com/developerworks/ru/library/j-5things1/)
+ [Java-online.ru](http://java-online.ru/blog-serialization.xhtml)
+ [Изучите секреты Java Serialization API](http://ccfit.nsu.ru/~deviv/courses/oop/java_ser_rus.html)
+ [JavaRush](http://bit.ly/1xwRA2D)
+ [Записки трезвого практика](http://www.skipy.ru/technics/serialization.html)
