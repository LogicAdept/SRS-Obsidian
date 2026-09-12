<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS

# What is Sass and SCSS?

> [!abstract] Short answer
> **Sass is a preprocessor language that extends CSS with variables, nesting, mixins, and functions; SCSS is its main syntax - a superset of CSS with curly braces.** Sass files compile to plain CSS before the browser ever sees them: the browser does not understand Sass natively.

## What it adds and how it builds

```scss
$brand: #0a5794;

@mixin centered($max: 60rem) {
  max-width: $max;
  margin-inline: auto;
}

.nav {
  @include centered(50rem);
  ul { list-style: none; }        /* nesting: compiles to .nav ul */
  a { color: $brand; }
}
```

**Listing 1.** SCSS: a variable, a parameterized mixin, and nesting - all resolved at build time into ordinary CSS.

The official guide's feature list - variables (`$name`), nesting, mixins (`@mixin`/`@include`), inheritance (`@extend`), operators, and modules - is exactly what modern *plain* CSS has been catching up with: custom properties, nesting, and `@layer` cover more and more of it, which is why adoption decisions today weigh "do we still need a build step".

> [!warning] Sass output is CSS - and nesting produces specificity
> Two traps. First, nothing runs in the browser until `sass input.scss output.css` (or a bundler) has compiled the file; debugging means looking at the *output*, not the source. Second, mechanical nesting compiles to descendant selectors - `.nav ul a` chains - whose specificity grows with depth and fights overrides; the same pain as id specificity (see [[What is the difference between an ID selector and a class selector in CSS]]). Style guides therefore cap nesting depth.

## The two syntaxes

`.scss` (SCSS) is the curly-brace, semicolon syntax - every CSS file is already valid SCSS, which made adoption friction-free. `.sass` is the original indented syntax: no braces or semicolons, structure by indentation - shorter for small files but unfamiliar to CSS readers. Both compile from the same engine; SCSS won the ecosystem because existing stylesheets import with zero edits.

Tooling-wise, compilation runs from the command line (`sass input.scss output.css`, with `--watch` for incremental rebuilds) or inside bundlers; source maps map the browser's CSS back to the SCSS lines that produced it - without them debugging a compiled stylesheet is guesswork. See [[What is CSS]] for the language it compiles into and [[What is a CSS selector]] - selectors themselves are unchanged by preprocessing.

> [!tip] Interview answer
> **Sass is the preprocessor; SCSS is its CSS-like curly-brace syntax (the .sass indented form is the alternative). It adds variables, mixins, nesting, and functions, and compiles to plain CSS in a build step. Modern CSS catches up with much of it, so the real cost is the build dependency - and deep nesting compiles to over-specific selectors.**
