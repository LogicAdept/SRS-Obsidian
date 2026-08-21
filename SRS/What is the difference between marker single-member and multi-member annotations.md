<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps:

- Marker: no elements; presence is the data (`@Override`, `@Deprecated` as used). Cleaner than `@Flag(true)`.
- Single-member: one element named `value`, used with the shorthand `@SuppressWarnings("unchecked")`.
- Multi-member: named elements, each `name =` when you set them (`minLength`, `maxLength`, `pattern`).

All three still need `@Retention` / `@Target` like any custom type if you declare your own.
> [!warning] Unverified traps from the dump
> - A single member not named value is not the single-member shorthand form.
> - Marker vs empty-body @interface with unused defaults: dumps treat “no elements” as the marker definition.
