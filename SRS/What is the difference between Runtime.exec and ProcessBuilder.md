<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS

# What is the difference between Runtime.exec and ProcessBuilder

> [!abstract] Short answer
> Both start an OS process and return a `Process`, but `Runtime.exec(String)` splits the command on whitespace, runs **no shell**, and is deprecated since Java 18 as error-prone. `ProcessBuilder` takes an explicit `List<String>` command plus configuration for the working directory, environment, and stream redirection (`redirectInput/Output/Error`, `inheritIO`), and its builder object is reusable. ProcessBuilder is the recommended API.

`exec(String)` tokenizes on whitespace only: an argument containing a space — a filename, a path — arrives as several separate arguments. And because no shell is involved, pipes, `;`, quotes, and `&&` are literal characters; `exec("date; date")` tries to execute a program literally named `date;` and fails with `IOException`. The array form `exec(String[])` is equivalent to ProcessBuilder's command list but offers none of its configuration.

## The tokenization failure in one run

One program shows both failure modes and the ProcessBuilder fix: `exec("cat my file.txt")` breaks the filename into three words, while `new ProcessBuilder("cat", "my file.txt")` keeps it as one argument and prints the file content.

```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class ExecTokenizationDemo {
    public static void main(String[] args) throws Exception {
        Path file = Path.of("my file.txt");
        Files.writeString(file, "file content");

        // 1) exec(String) splits on whitespace: cat receives three words
        try {
            Process p = Runtime.getRuntime().exec("cat my file.txt");
            p.waitFor();
            System.out.println("exec(String) exit = " + p.exitValue());
            new String(p.getErrorStream().readAllBytes()).lines()
                    .filter(s -> s.contains("No such file")).limit(2)
                    .forEach(s -> System.out.println("  stderr: " + s.trim()));
        } catch (IOException e) {
            System.out.println("exec(String) threw " + e.getClass().getSimpleName());
        }

        // 2) ProcessBuilder keeps "my file.txt" as ONE argument
        Process p2 = new ProcessBuilder("cat", "my file.txt").start();
        p2.waitFor();
        System.out.println("ProcessBuilder exit = " + p2.exitValue());
        System.out.println("ProcessBuilder stdout = "
                + new String(p2.getInputStream().readAllBytes()).trim());

        // 3) no shell: ";" is an ordinary character, so the program name is wrong
        try {
            Runtime.getRuntime().exec("date; date");
        } catch (IOException e) {
            String msg = e.getMessage().split("\n")[0];
            System.out.println("exec(\"date; date\") threw IOException: " + msg);
        }

        Files.deleteIfExists(file);
    }
}
// Output (JDK 21):
// exec(String) exit = 1
//   stderr: cat: my: No such file or directory
//   stderr: cat: file.txt: No such file or directory
// ProcessBuilder exit = 0
// ProcessBuilder stdout = file content
// exec("date; date") threw IOException: Cannot run program "date;": Exec failed, error: 2 (No such file or directory)
```

**Listing 1.** Same filename, two APIs: whitespace tokenization turns one argument into three and fails; the builder's explicit list succeeds; the shell command `date; date` never reaches a shell at all.

```d2
direction: right
s: "exec(String)\ndeprecated since Java 18" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}
tok: "Whitespace tokenizer\nno shell, no quoting" {
  width: 260
  height: 90
  style.fill: "#ffcdd2"
}
pb: "ProcessBuilder\nList command · directory · env\nredirectInput/Output/Error · inheritIO" {
  width: 330
  height: 120
  style.fill: "#e8f5e9"
}
pr: "Process\nstreams · waitFor · onExit" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
s -> tok
pb -> pr
```

**Fig. 1.** The string form loses information in tokenization; the builder passes the exact argument list and adds configuration.

> [!warning] The myth of the implicit shell
> Neither API uses a shell — "it runs like in terminal" is the popular lie. Quoting inside `exec("...")` is not parsed, globbing does not expand, and piping needs an explicit `sh -c` command built as a ProcessBuilder list. The second trap: forgetting to drain child output — a full pipe buffer blocks the child on write; redirect to files, use `inheritIO`, or read the streams concurrently, see [[How do you invoke an external process in Java]].

Passing variables into the child's environment is a separate skill card — [[How do you pass environment variables to a subprocess in Java]] — and the modern handle-based view of processes is [[What is ProcessHandle]].

> [!tip] Interview answer
> `Runtime.exec(String)` is the legacy convenience: it blindly splits the command on whitespace, has no shell, and is deprecated since Java 18. `ProcessBuilder` takes the exact argument list and adds the working directory, environment, and stream redirection, and one builder can start several processes. For anything with spaces in arguments or any stream handling, ProcessBuilder is the only sane choice.

