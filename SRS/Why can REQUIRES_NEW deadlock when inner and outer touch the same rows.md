<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The outer transaction stays suspended but still holds its locks and connection. The inner REQUIRES_NEW transaction then tries to lock the same rows. Those locks are not released until the outer transaction resumes and completes, so the inner transaction can wait forever on the suspended outer one.
> [!warning] Unverified traps from the dump
> - Do not use REQUIRES_NEW to update the same tables the parent transaction already locked.
> - Connection-pool exhaustion is a related failure when many threads each need that second connection.
