<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Drive a service that writes business data in REQUIRED and audit in REQUIRES_NEW, then fail the outer method. After the test transaction/rollback of the caller, assert the audit row is still in the database and the business row is not. A separate test can call a MANDATORY method with no transaction and expect IllegalTransactionStateException.
> [!warning] Unverified traps from the dump
> - A class-level @Transactional on the test itself can swallow REQUIRES_NEW independence unless the test is designed to see a real commit.
> - Self-invocation in the service under test will make REQUIRES_NEW look like REQUIRED.
