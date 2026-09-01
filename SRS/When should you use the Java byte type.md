<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A `byte` is an 8-bit signed two's-complement integer with range -128 to 127 (default field value 0). Dumps recommend it when you need to save memory and every value stays in that range — especially large arrays — and when you are dealing with raw binary, file, image, or network bytes.
> [!warning] Unverified traps from the dump
> - Arithmetic still promotes byte to int, so byte a + byte b is an int.
> - byte is signed; 128 and above need a cast and wrap.
