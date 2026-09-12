<!--
reps: 0
priority: 0
-->
#DevOps/Shell #OperatingSystems/Linux #SRS

# What is a Unix shell

> [!abstract] Short answer
> A **shell** is a command language interpreter: a program that reads text commands — interactively from a terminal or from a script file — expands them, executes them, and reports results and exit status. It is simultaneously the user's interface to the operating system and a small programming language with variables, pipes, redirection, and control flow. `sh` names the POSIX command language; bash and zsh are implementations of it with extensions.

POSIX defines the shell as "a command language interpreter" that "may operate on an input stream or ... interactively prompt and read commands from a terminal" — both modes are the same language. In **interactive** mode the shell prints a prompt (PS1), reads a line, performs expansion (parameters, globs, command substitution), executes the resulting pipeline, and reports the exit status in `$?`. In **non-interactive** mode — a script — the same interpreter reads commands from a file, no prompt, with `$0` naming the script and arguments in `$1`...; this is the mode that turns shell into automation glue, and the one CI pipelines use when they call `sh` steps (see [[What is a Jenkins Pipeline]]). An **interactive shell** is defined simply as "a processing mode of the shell that is suitable for direct user interaction", and it is where job control lives ([[How do you run a command in the shell as a background job]]).

```bash
#!/bin/sh
# Conceptual: the shell as automation language
set -eu                       # fail on error, unset variables
log=/tmp/deploy.log
count=$(ls /srv/app | wc -l)  # command substitution
echo "releases: $count" >> "$log"
if [ "$count" -gt 5 ]; then
  rm -rf /srv/app/old_*       # glob expansion + redirection
fi
```

**Listing 1.** The ingredients that make the shell a language: substitution, pipelines, redirection, tests, and exit-status discipline.

## The interpreter's place in the system

The shell sits above the kernel's process and file APIs: it forks and execs external utilities (`ls`, `grep`, `df`), routes standard streams between them with pipes, and glues them into pipelines whose expressive power comes from composition rather than from the shell itself. Startup files differ by mode — interactive shells read profile/rc files; an interactive shell expands `$ENV` for per-user setup — which is why behavior sometimes differs between "works in my terminal" and "fails in CI": CI runs non-interactive, non-login shells with no rc files.

> [!warning] "bash" and "shell" are not synonyms
> `sh` is the POSIX shell command language; bash ("Bourne again shell"), dash, zsh, and ksh are implementations. The classic failure: a script with `#!/bin/sh` that uses bash-only features (arrays, the double-bracket extended test keyword, `==` glob matching) — it works on a machine where /bin/sh links to bash and breaks where /bin/sh is dash (Debian/Ubuntu). Either write POSIX-compatible sh or declare `#!/bin/bash` explicitly. The second trap is calling the shell "just a terminal": the terminal is the I/O device; the shell is the interpreter behind it, and the same interpreter runs headless in scripts and CI.

> [!tip] Interview answer
> **A Unix shell is a command language interpreter: it reads commands interactively from a terminal or non-interactively from scripts, expands them, and executes pipelines of external utilities while managing standard streams and exit statuses. sh is the POSIX language specification; bash and zsh are implementations. Interactive mode adds prompts, startup files, and job control; scripts run the same language headless — which is why sh-compatible syntax versus bashisms is the classic portability pitfall.**
