<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# How do you create a mailto link in HTML?

> [!abstract] Short answer
> **An email link is an `<a>` whose `href` uses the `mailto:` URL scheme followed by the address**: `<a href="mailto:user@example.net">Write me</a>`. Activation does not navigate anywhere - it launches the user's registered mail client with the To field prefilled.

## The mailto URL and its parameters

```html
<a href="mailto:m.bluth@example.com">Email</a>
<a href="mailto:boss@example.com?cc=hr@example.com&subject=Raise&body=As%20discussed...">Ask for a raise</a>
```

**Listing 1.** Plain mailto and one with header parameters; multiple addresses are comma-separated.

Everything after the address is a query string with standard header parameters: `subject`, `cc`, `bcc`, and `body`. Values must be URL-encoded - a space becomes `%20` (see [[What is URL encoding and how do you perform it in Java]] for the encoding machinery), and `&` separates parameters.

> [!warning] mailto has no fallback and no delivery guarantee
> The scheme only delegates to whatever handler the OS registered as the mail client. In a browser without a configured mail program the click does nothing useful - which is why production "contact us" flows usually prefer a form plus a server-side sender. And nothing about mailto implies the message was ever sent; it merely drafts one.

## Encoding inside the href attribute

Two encodings meet in one attribute, and both matter. The URL itself needs percent-encoding for spaces and special characters in `subject` and `body`; and because `&` separates parameters, an HTML source file must write it as the entity `&amp;` - the character reference rules from [[What is an HTML character entity]] apply inside every attribute value.

```html
<a href="mailto:boss@example.com?subject=Q2%20report&body=See%20attached">Send</a>
```

**Listing 2.** The attribute source uses &amp; and %20; the DOM href value holds the decoded characters.

## Practical parameters

The four standard parameters are `subject`, `cc`, `bcc`, and `body`. Several recipients in one field are comma-separated with no space after the comma. Long prewritten bodies are legal but fragile - mail clients reflow or re-encode them - so keep body text short and put detail in the application, not the link. The same anchor can offer both channels at once, for example a `mailto:` link plus a `tel:` link in one contact block.

The `<a>` element page lists `tel:` as the sibling scheme for phone numbers - same delegation model, no navigation (see [[How do you specify a hyperlink destination in HTML]]).

> [!tip] Interview answer
> **Use an anchor with href="mailto:address"; append ?subject=...&cc=...&body=... as URL-encoded parameters to prefill the draft. It opens the local mail client rather than a web page, so there is no in-browser fallback and no delivery guarantee - the pattern is for contact pages, not for critical flows.**
