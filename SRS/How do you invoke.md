<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как вызвать хранимую процедуру?**

__Хранимые процедуры__ – это именованный набор операторов SQL хранящийся на сервере. Такую процедуру можно вызвать из Java-класса с помощью вызова методов объекта реализующего интерфейс `java.sql.Statement`.

Выбор объекта зависит от характеристик хранимой процедуры:

+ без параметров → `Statement`
+ с входными параметрами → `PreparedStatement`
+ с входными и выходными параметрами → `CallableStatement`

> Если неизвестно, как была определена хранимая процедура, для получения информации о хранимой процедуре (например, имен и типов параметров) можно использовать методы `java.sql.DatabaseMetaData` позволяющие получить информацию о структуре источника данных.

Пример вызова хранимой процедуры с входными и выходными параметрами:

```java
public vois runStoredProcedure(final Connection connection) throws Exception {
    // описываем хранимую процедуру
    String procedure = "{ call procedureExample(?, ?, ?) }";

    // подготавливаем запрос
    CallableStatement cs = connection.prepareCall(procedure);

    // устанавливаем входные параметры
    cs.setString(1, "abcd");
    cs.setBoolean(2, true);
    cs.setInt(3, 10);

    // описываем выходные параметры
    cs.registerOutParameter(1, java.sql.Types.VARCHAR);
    cs.registerOutParameter(2, java.sql.Types.INTEGER);

    // запускаем выполнение хранимой процедуры
    cs.execute();

    // получаем результаты
    String parameter1 = cs.getString(1);
    int parameter2 = cs.getInt(2);

    // заканчиваем работу с запросом
    cs.close();
}
```
