<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `IndexOutOfBoundsException` is the general unchecked type for an index that is out of range (array, string, or list-like structure). `ArrayIndexOutOfBoundsException` and `StringIndexOutOfBoundsException` are the specialized subclasses for arrays and strings. List `get`/`set` typically throw the parent `IndexOutOfBoundsException`.
> [!warning] Unverified traps from the dump
> - catch (IndexOutOfBoundsException e) also matches ArrayIndexOutOfBoundsException.
> - String.charAt with a bad index is StringIndexOutOfBoundsException, not ArrayIndexOutOfBoundsException.
