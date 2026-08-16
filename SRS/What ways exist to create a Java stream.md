<!--
reps: 0
priority: 0
-->
#Java/Streams #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие существуют способы создания стрима?**

1. Из коллекции:
```java
Stream<String> fromCollection = Arrays.asList("x", "y", "z").stream();
```
2. Из набора значений:
```java
Stream<String> fromValues = Stream.of("x", "y", "z");
```
3. Из массива:
```java
Stream<String> fromArray = Arrays.stream(new String[]{"x", "y", "z"});
```
4. Из файла (каждая строка в файле будет отдельным элементом в стриме):
```java
Stream<String> fromFile = Files.lines(Paths.get("input.txt"));
```
5. Из строки:
```java
IntStream fromString = "0123456789".chars();
```
6. С помощью `Stream.builder()`:
```java
Stream<String> fromBuilder = Stream.builder().add("z").add("y").add("z").build();
```
7. С помощью `Stream.iterate()` (бесконечный):
```java
Stream<Integer> fromIterate = Stream.iterate(1, n -> n + 1);
```
8. С помощью `Stream.generate()` (бесконечный):
```java
Stream<String> fromGenerate = Stream.generate(() -> "0");
```
