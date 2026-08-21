<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps list compile-time checked types as: IOException, FileNotFoundException, ClassNotFoundException, InterruptedException, SQLException, ParseException.

Stock example: FileInputStream / FileReader on a missing file throws FileNotFoundException. The method must catch it or declare throws FileNotFoundException (or a supertype such as IOException).
> [!warning] Unverified traps from the dump
> - FileNotFoundException extends IOException; listing both is a parent-child pair, not two unrelated branches.
> - ClassNotFoundException is checked; NoClassDefFoundError is an Error and is not checked.
