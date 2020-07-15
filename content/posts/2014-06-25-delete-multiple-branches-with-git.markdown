---
categories:
- git
- Self-Reference
comments: true
date: 2014-06-25
layout: post
title: Delete multiple branches with git
---

When working on projects with multiple developers following a feature branching
workflow, you can end up with a lot of branch laying around. I've been trying to
optimize my branch cleanup workflow for a while now and had a big breakthrough
recently.

<!-- more -->

__UPDATE:__ I now use a [shell
script](https://github.com/pengwynn/dotfiles/blob/master/bin/git-sweep)
which has the meat of the git-sweep functionality. Thanks to @pengwynn
for letting me steal that.

Before we get to that, I must mention [git-sweep](http://lab.arc90.com/2012/04/03/git-sweep/).
It has been revolutionary to keeping branches (both locally and remote) clean.
If you care at all about the output of `git branch`, install that now.

However, there's another simpler trick I just recently discovered. Deleting
multiple local branches with one command.

    $ git branch -D old-branch-1 old-branch-2

That's it! Simply pass as many branches into `branch -D` as you want and `git`
will gladly delete them all.

### But why do you need this?

I just said that `git-sweep` cleans up local and remote branches after they are
merged into `master`. So, why would we ever need to delete local branches? For
one, you might not merge branches into master, but still want to delete them.
But more likely, you'll need to do this after pulling down a colleague's branch
to review. Once you give them the green light, it's best practice for them to
rebase onto `master` (interactively to prevent accidentally merging `!fixup`
commits). However, you will have one state of the branch locally, but they've
merged a different, rebased state. This is just enough of a change to fool
`git-sweep`, and `git` herself, into missing the fact that these branches are
the same. Luckily, there is a quick way to identify and remove those branches
too.

Handily, `git-branch` has a super verbose mode which can be shown with the
"double v" flag (`-vv`). This displays the branch name, HEAD commit, remote
tracking branch, and HEAD commit message.

    $ git branch -vv
    * gh-pages 123456 [origin/gh-pages] Show new features on the project website
      master   654321 [origin/master] Merge features/super-new-feature into master

Additionally, super verbose mode will also show us when a remote tracking branch
disappears (is deleted). Immediately following the tracking branch name, we'll
notice a "gone".

    $ git branch -vv
    * master      654321 [origin/master] Merge features/super-new-feature into master
      old-feature 523621 [origin/old-feature: gone] Users can see the brand new feature

I like to `grep` for that and filter out the branches which I don't want to
delete. Basically, my whole cleanup procedure goes like this:

    $ git branch -vv | grep gone]

      old-feature-1 523621 [origin/old-feature-1: gone] Link to the new account page
      old-feature-2 856956 [origin/old-feature-2: gone] Toggle turtle visibility with feature flag

    $ git branch -D old-feature-1 old-feature-2
    Deleted branch old-feature-1 (was 523621).
    Deleted branch old-feature-2 (was 856956).

And there you have it, removing multiple branches in git with a bonus of
finding branches who've lost their remote tracks.

Happy branching!!

-- Chris

