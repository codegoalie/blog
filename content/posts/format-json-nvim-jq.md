+++
date = "2024-02-12T16:09:11-05:00"
title = "Format JSON in Nvim with jq"
categories = ["TIL"]
draft = false
+++

I often get large JSON files which contain no newlines or indentation. I'd like
to look at these reasonably in neovim, but it's been cumbersome until today.

TL;DR: You can replace the contents of the buffer with output formatted by jq
with one command: `:%!jq .`

<!--more-->

Other techniques I've used, from worse to lest worse:

1. Replacing every `,` with `,\r` and then using `=` to auto-indent the lines.
   This rarely works well.
1. Using `jq` externally. `cat input.json | jq . > output.json`. This kind of
   sucks because you now have 2 files...

Now, you can open the file in neovim and type `:%!jq .`. Magically, the buffer
will be nicely formatted.

Roughly, this is entering a command, `:`, on the whole buffer, `%`, then
executing a shell command, `!`, of `jq .` the most basic `jq` invocation.
Presumably, you could entry and `jq` filter command to form some other JSON
instead of just formatting the given JSON, but I'll leave that up to you to play
with.

Happy formatting!!

-- Chris
