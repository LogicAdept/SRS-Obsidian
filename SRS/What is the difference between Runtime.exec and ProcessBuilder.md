<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps present `Runtime.exec` as the older convenience method and `ProcessBuilder` as the recommended API for command tokens, working directory, environment, and I/O redirection (including pipelines). They claim `exec` is implemented by building a ProcessBuilder and calling `start()`.

`exec` takes a single command string (tokenized) or a string array plus optional envp and directory. ProcessBuilder keeps tokens as a list, exposes `environment()`, `directory()`, and redirects, then `start()`.
> [!warning] Unverified traps from the dump
> - A non-null envp on exec can replace the child's whole environment instead of editing a copy; ProcessBuilder.environment() starts from a copy of the current environment.
> - Neither API invokes a shell unless you explicitly start sh -c or cmd.exe.
