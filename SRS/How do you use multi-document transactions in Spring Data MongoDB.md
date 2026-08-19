<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #Java/Spring/Transactions #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Register a MongoTransactionManager bean, then put @Transactional on a service method. Spring binds a ClientSession to the thread and commits or rolls back around the method.

The deployment must be a replica set or sharded cluster. Standalone mongod does not support transactions.

```java
@Bean
MongoTransactionManager transactionManager(MongoDatabaseFactory dbFactory) {
    return new MongoTransactionManager(dbFactory);
}

@Transactional
public void transferFunds(String fromId, String toId, BigDecimal amount) {
    accountRepo.debit(fromId, amount);
    accountRepo.credit(toId, amount);
}
```
> [!warning] Unverified traps from the dump
> - Standalone MongoDB cannot run multi-document transactions.
> - MongoDB transactions since v4.0 are not enabled by default in comparison dumps.
