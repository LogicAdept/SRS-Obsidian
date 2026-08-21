<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

SUPPORTS joins the current transaction when one exists and otherwise runs with no transaction. Interview dumps treat it as the option for work that can participate in a caller transaction but does not need to start one, often read-style methods.
> [!warning] Unverified traps from the dump
> - With a synchronizing transaction manager, SUPPORTS is not identical to 'no @Transactional': the scope can still share a JDBC Connection or Hibernate Session.
> - Standalone SUPPORTS writes auto-commit statement by statement; there is no unit-of-work rollback.
