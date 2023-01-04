+++
date = "2023-01-04T14:35:12-05:00"
title = "One-liner to copy a Github PR link from the terminal"
categories = ["git", "Command-Line"]
draft = true
+++

Here's a super quick one-liner to copy the current branch's PR URL to your
clipboard (for posting into Slack, tickets, etc.)

```bash
$ gh pr view --json url --jq .url | <pbcopy | xclip -sel c>
```

Remember to replace the copy command with your platform's specific command.

This would also make a good shell alias.

Also, also, I might try setting up [Clipboard][1] for multi-platform goodness.

Happy PR-ing!

-- Chris

[1]: https://github.com/Slackadays/Clipboard
