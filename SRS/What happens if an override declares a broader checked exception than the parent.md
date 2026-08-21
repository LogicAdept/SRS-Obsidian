<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: compile error.

Invalid examples: parent throws FileNotFoundException, override throws IOException; parent throws IOException, override throws Exception. A Super-typed call only requires catching the narrower type, so a broader checked exception could escape.

Same rejection for an unrelated checked type: parent throws IOException, override throws SQLException.
> [!warning] Unverified traps from the dump
> - Exception is broader than IOException even though both are checked.
> - The restriction is checked-only; adding extra RuntimeException types on the override is allowed.
