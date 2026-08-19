<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

InterviewBit dump: SessionManagementFilter plus SessionAuthenticationStrategy cover timeouts, concurrent sessions, and session-fixation (migrateSession / newSession / none).
> [!warning] Unverified traps from the dump
> - migrateSession in a misconfigured cluster is a dump story for users seeing each other’s data. newSession is the safer fixation default in many lists.
