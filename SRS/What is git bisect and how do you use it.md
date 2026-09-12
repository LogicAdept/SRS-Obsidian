<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What is git bisect and how do you use it

> [!abstract] Short answer
> `git bisect` is a **binary search over commit history** for the commit that introduced a regression. You give it one known-bad and one known-good revision; it checks out the midpoint, you (or a script) declare pass/fail, and it halves the range each step — finding the first bad commit among N commits in ~log₂ N checks. `git bisect run <cmd>` automates the whole search: the command's exit code is the verdict (0 = good, non-zero = bad), and bisect prints the culprit commit and stops.

## Automated bisect, verbatim

```text
$ git bisect start HEAD HEAD~6
Bisecting: 2 revisions left to test after this (roughly 2 steps)
[0933e89…] Revision 4
$ git bisect run /tmp/bisect_test.sh
running /tmp/bisect_test.sh
Bisecting: 0 revisions left to test after this (roughly 1 step)
[6b84a0e…] Revision 6
running /tmp/bisect_test.sh
Bisecting: 0 revisions left to test after this (roughly 0 steps)
[b8cd78b…] Revision 5
running /tmp/bisect_test.sh
b8cd78b073838e32f53cadc688737e8cd27617a5 is the first bad commit
bisect found first bad commit
$ git bisect reset
Previous HEAD position was b8cd78b Revision 5
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim, hashes abridged): 7 commits, bug introduced at Revision 5 — the search checked Revision 4 (good), 6 (bad), 5 (bad) → verdict. Seven commits needed three checks; a month of history needs ten.

The manual flow behind it: `git bisect start <bad> <good>` → Git checks out the midpoint → you build/test → `git bisect good` or `git bisect bad` → repeat → `git bisect reset` to return to your branch. The verdict command can be anything scriptable: a unit test (`mvn -q test -Dtest=FailingCase`), a build (`./gradlew compileJava`), even a grep for the bad behavior. `git bisect log` records the session (save/share it); `git bisect skip` skips untestable commits (build broken at that commit) at the cost of some precision; `git bisect start HEAD v2.0` anchors the good side on a release tag ([[What is a tag in Git and how does it differ from a branch]]).

## Where bisect shines in backend work

The killer use case is a **regression that tests exist for**: "this endpoint started returning 500 after last week's merges" — bisect with `run` pointing at the integration test finds the commit without human reading. It also works on *behavioral* bugs with a manual loop, and on flaky-looking CI by bisecting the *test* against a fixed codebase. Compose with modern tooling: `git bisect run ./gradlew test --tests 'PaymentFlowTest'` in CI debug sessions, or bisecting *rebuilds* of an artifact to find which dependency bump broke the build.

> [!warning] Bisect only works if the good point is actually good — and it checks out commits *in place*
> If your "known good" revision secretly had the bug, the search converges to a wrong (usually the oldest) commit — verify the good state reproduces expected behavior *before* trusting the verdict. Requirements that trip teams: the project must *build* at intermediate commits (bisect checks out history as it was — migrations, generated code, and submodule pins must be consistent per commit; [[What are Git submodules and when do you use them]] matters here); tests must be deterministic — a flaky test turns the search into noise. You are left in **detached HEAD** during the session ([[What is HEAD and what is a detached HEAD]]) — finish with `reset`, and commit nothing mid-search. Merge-heavy histories narrow what "the first bad commit" means: the culprit found is on the *linearized* path bisect walks ([[How can you refer to a commit in Git]]'s ancestry syntax is what it explores).

```d2
direction: down
start: "bisect start bad-tip good-rev\nrange: N commits" {
  width: 340
  height: 100
  style.fill: "#e3f2fd"
}
mid: "checkout midpoint\ntest / run script" {
  width: 320
  height: 100
  style.fill: "#fff3e0"
}
branch: {
  good: "good -> range halves right" {
    width: 300
    height: 80
    style.fill: "#e8f5e9"
  }
  bad: "bad -> range halves left" {
    width: 300
    height: 80
    style.fill: "#ffebee"
  }
}
verdict: "first bad commit printed\nbisect reset returns to work" {
  width: 400
  height: 100
  style.fill: "#e8f5e9"
}
start -> mid
mid -> good
mid -> bad
good -> verdict
bad -> verdict
```

**Fig. 1.** Each verdict halves the remaining range — log₂(N) steps to the exact introducing commit, by script or by hand.

> [!tip] Interview answer
> **git bisect binary-searches history for the commit that introduced a regression: start with one bad and one good revision, mark each checked-out midpoint good or bad — or hand the verdict to a script with bisect run, whose exit code decides — and it reports the first bad commit in log-two-N steps, then reset returns you to your branch. The requirements are a buildable history and a deterministic test, a genuinely good anchor, and awareness that you sit detached during the search. It is the tool for 'this worked last week' regressions when tests exist to encode the symptom.**

