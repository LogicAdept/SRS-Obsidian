<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Query by Example builds a query from a populated domain object (the probe) and an ExampleMatcher. You do not write field names in a query string. Null properties are ignored. JpaRepository inherits this via QueryByExampleExecutor; MongoRepository does too.

```java
Employee probe = new Employee();
probe.setDepartment("Engineering");
probe.setActive(true);
ExampleMatcher matcher = ExampleMatcher.matching()
    .withIgnorePaths("id")
    .withStringMatcher(StringMatcher.CONTAINING)
    .withIgnoreCase();
Example<Employee> example = Example.of(probe, matcher);
List<Employee> employees = employeeRepository.findAll(example);
```
> [!warning] Unverified traps from the dump
> - Ignore the id path or an unset identifier can distort the match.
> - Mongo dumps add a default _class restriction on typed Example matching.
