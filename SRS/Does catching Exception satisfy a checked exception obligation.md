<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: yes. catch (Exception e) is listed as one way to handle several checked types at once, because Exception is the parent of IOException, SQLException, and the other checked types (and of RuntimeException).

Dumps still prefer specific handlers. catch (Exception e) compiles even when the try throws no checked exception, because Exception also covers RuntimeException.
> [!warning] Unverified traps from the dump
> - catch (IOException e) does not compile if the try cannot throw IOException or a related checked type (unreachable catch). catch (Exception e) is excluded from that rule.
> - Catching Exception also swallows RuntimeException; dumps call that too broad.
