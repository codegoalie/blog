---
categories:
- Command-Line
comments: true
date: 2014-08-25
layout: post
title: Useful command line expansions
---

Here's a quick trick I've been using for a while, but have found that not many
others know about it. It's a way to grab the arguments from the last command you
executed. Command line expansion allows you to [do many
things](http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_03_04.html), but
today we'll focus on just argument expansion.

<!-- more -->

First to simply repeat the last command with `!!`. This is most helpful when
needing to prefix a command; with something like `sudo` or `bundle exec`.

```
$ mv /really/long/path/with/more/dirs/file /another/deeply/nested/dir/structure
mv: cannot move `...' to `...': Permission denied

$ sudo !!
```

Learn more about bang-bang on [episode 32 of sysadmin
casts](https://sysadmincasts.com/episodes/32-cli-monday-history).

Expanding on this concept, how about only part of the previous command? The
`!$` history expansion expands to the last argument (or token) from the previous
command. Working off the previous example, if we now want to edit that freshly
moved file:

```
$ vim !$
```

which expands to

```
$ vim /another/deeply/nested/dir/structure
```

Quick and easy! There are many ways to use history expansion to get parts of the
previous (and others from history) command. `!$` is by far the one I use the
most. You'll do yourself a huge favor to commit that to muscle memory.

To get an argument other than the last, you can use `!:x` where `x` is the (0
based) index of the arguemnt, or a range, or `*` to get all the arguments.

```
$ vim /another/deeply/nested/dir/structure
$ git checkout -b features/laser-sharks

  !:2     => -b
  !:0     => git
  !:$     => features/laser-sharks
  !:^     => checkout
  !:1-2   => checkout -b
  !:-2    => git checkout -b
  !:2-$   => -b features/laser-sharks
  !:*     => checkout -b features/laser-sharks
```

> ZSH power tip: Tapping `tab` with any of these expansions in ZSH will expand
  them inline to preview before executing.

Happy history-ing!  

-- Chris
