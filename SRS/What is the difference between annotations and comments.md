<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# What is the difference between annotations and comments?

> [!abstract] Short answer
> **Comments** (`//` and `/* … */`) are **lexical noise**: the compiler **discards** them before parsing. **Annotations** (`@Name`) are **real syntax** — typed metadata on declarations (and type uses). Tools, the compiler, processors, and (if `RUNTIME`) reflection can read them. A comment never fails compilation for a wrong `@Override`; an annotation can.

## Discarded text vs language constructs

After Unicode and escape translation, comments are **thrown away** with white space. Only tokens remain. That is why `// @Override` does nothing: the `@` never becomes an annotation. `/** … */` is still a **traditional comment** (`/**` is not a third comment kind). Javadoc is a **separate** program that scrapes those comments from source; it is not the compiler treating them as metadata.

An annotation is an `@` followed by an annotation type (an `@interface`). It has elements with types and optional defaults. The compiler checks applicability (`@Target`), retention, and special contracts such as [[How does the Override annotation work]]. Processors and runtime reflection see annotations; they never see comments. See [[What is a Java annotation]] and [[How do annotation processors differ from runtime reflection]].

Oracle’s classic `ClassPreamble` example is the contrast in one picture: a block of author/date `//` lines is replaced by an `@interface` plus an instance so a tool can read `author()` instead of grepping English.

```java
// Author: Jane Doe — discarded; no program can query this

@ClassPreamble(author = "Jane Doe", reviewers = {"Alex"})
class Ledger { }
```

**Listing 1.** Same human story; only the annotation is a typed construct.

```d2
direction: down
src: "source: // note  and  @Override" {
  width: 280
  height: 50
}
lex: "lexer discards comments" {
  width: 280
  height: 50
}
tok: "tokens include @ Override" {
  width: 280
  height: 50
}
src -> lex -> tok
```

**Fig. 1.** Comments never reach the parser; annotations do.

> [!warning] Javadoc tags are still comments
> `@param` / `@return` live **inside** `/** … */`. They are not annotation types. `@Documented` only asks Javadoc to **copy** a real annotation into generated HTML; it does not promote a comment into an annotation, and it does not make `// @Override` check anything.

> [!tip] Interview answer
> Comments are stripped in lexical analysis; the compiler never sees them. Annotations are part of the program: typed, targeted, optionally retained for processors or reflection, and able to fail the build (Override is the usual example). Javadoc comments look similar because they use @ tags, but those tags are still comment text unless you declare a real @interface.
