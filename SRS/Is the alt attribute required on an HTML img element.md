<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# Is the alt attribute required on an HTML img element?

> [!abstract] Short answer
> **Yes - the standard requires every `<img>` to carry an `alt` attribute, and MDN calls it mandatory.** Its value is the textual replacement for the image: screen readers read it out, and browsers display it when the image cannot load. For purely decorative images the required value is the empty string `alt=""` - present but empty, which is different from omitting the attribute.

## What the attribute must contain

```html
<img src="chart.png" alt="Sales grew 12 percent in Q2">   <!-- meaningful image: describe it -->
<img src="divider.png" alt="">                            <!-- decorative: announce nothing -->
<img src="logo.png" alt="ACME home">                      <!-- logo linking home: name the destination -->
```

**Listing 1.** Three alt strategies: description, empty for decoration, destination name for an image that acts as a link.

The replacement text must do the image's job in text form. A rule of thumb from accessibility guidance: write what a person would need to get the same information, not "image of..." (the screen reader already announces it is an image).

> [!warning] alt="" and a missing alt are not the same
> An empty alt tells assistive technology to skip the image; a missing alt makes the browser fall back to announcing the file name or URL, which is noise for screen-reader users. The standard has narrow carve-outs where alt may be omitted (for example captioned images inside a `<figure>`), but treating "required with a meaningful value, or empty when decorative" as the rule is the correct engineering default.

When an image fails to load, the replacement text appears with a broken-image indicator - the same mechanism that makes alt text survive link rot, content blocking, or a failed network fetch. For the element anatomy see [[What is HTML]]; for an image that navigates see [[How do you specify a hyperlink destination in HTML]].

## How screen readers use it

A screen reader announces the image and reads the alt value in the same breath, so the value is the image's voice in the accessibility tree. Phrases like "photo of" duplicate what the technology already announces; what matters is the information the image carries - a chart's trend, a button's action, a logo's organization. Empty alt removes the image from that tree entirely, which is exactly right for spacers and decorative dividers and wrong for an informative diagram.

> [!tip] Interview answer
> **Yes, alt is required: it is the image's text replacement for screen readers and for load failures. Decorative images take an empty alt="", meaningful images take a description of their content or function. Omitting the attribute entirely is a conformance error and degrades accessibility.**
