---
categories:
- git
- Pull Requests
comments: true
date: 2013-04-04
layout: post
title: Better pull requests with git --autosquash
---

**UPDATE (Jun 7, 2013):** I created an [ascii.io video demo of
autosquash](http://ascii.io/a/3467) for your viewing pleasure.

Pull requests are an extremly crucial part of our workflow at Mobile
Defense. We pride ourselves on producing quality code and we do not
subscribe to the git-blame "I didn't write it" culture. We all take
responsibility for all the code we produce, as a team. As such, being
able to review our code efficiently and thoroughly **before** it gets
into `master` is a goal we are constantly looking to improve upon.

A somewhat paradox in reviewing code arises when the need for reviewers
to see the updates based on their feedback quickly and efficiently and
for the developer to be able to 'fixup' their branch before merging to
ensure the code enters `master` as cleanly as possible. That's where
git-rebase comes in.

Rebase is an extremely powerful tool in the git toolbelt. Combine
commits, edit commits in-place, rewrite history, etc. It's especially
great for cleaning up your topic branches before submitting for code
review. However, remembering which commits need to be squashed into which
can be tricky especially when being the reviewee and the reviewer on
multiple pull requests daily. Well, it turns out git already has a really
clever, built-in way to organize and automate the branch cleanup process.
It is perfectly suited for making changes based on pull request feedback.
It's called autosquash.

<!-- more -->

Here was a typical pull request workflow:

1. Code up a feature; commit early and often.
1. Push to github and open a pull request.
1. Do a quick self-review of my code.
1. Ask others to review my code.
1. Add temporary commits in response to comments.
1. When the branch is approved for merge, rebase and fixup the
   temporary commits into the original commits.
1. Merge the branch.

As you might have experienced or noted in the workflow above, how do you
keep organized and remember which temporary commits should be squashed
into which original commits? The problem I ran into time and time
again was that as soon as I started an interactive rebase I would be
unable to remember exactly which commits needed to be changed, squashed,
or fixedup. So, I had been developing some commit message conventions for
temporary commits.

For example, a commit which I knew was incomplete work or needed to be
looked at again would have it's message prefixed with an excalmation
mark.

    ! Possible logic error in the complex_redirect logic

Further, commits which I knew I wanted to squash into previous commits
would be prefixed with four hyphens and have a message which I would be
able to make sense of when editing the rebase todo file.

    ---- into the first set of unit tests

This worked fairly well as long as I left myself good notes. But, surely
there must be a better way!

## Enter autosquash

The `--autosquash` flag on git-rebase is exactly what I was looking
for. During an interactive rebase, it processes messages to stage squashes
and fixups. These messages are setup with flags on git-commit at commit
time, which is when you are most likely to know what you ultimately
intend to do with commits. Further, it works via the commit message
so it's easy for humans to understand as well!

Say you have a feature branch with three commits: (viewing git logs with
the [incredibly awesome lg
alias](/2013/02/08/help-i-lost-a-commit-from-days-ago/#lg))

    * cdaa049 (HEAD, features/new_hotness) Add new hotness to UI (66 seconds ago) <Chris Marshall>
    * e14aa92 Implement new hotness backend (2 minutes ago) <Chris Marshall>
    * 293070e Ensure new hotness works (2 minutes ago) <Chris Marshall>
    * de72adc (origin/master, origin/HEAD, master) Add git internals meetup talk slides (6 months ago) <Chris Marshall>

Now let's say you get a review comment on the commit for the tests
('Ensure ...') which asks to add a test for a missed edge case.

So we will code up our edge case fix and as we commit, we'll add the
flag to specify what we ultimately will do with the commit.

Git-commit has two such flags: `--fixup` and `--squash` with each of these
we will specify the commit **into which** we want to fixup or squash. In
our example, we want to fixup into the first commit after master:
`293070e`.

We can do that with:

    $ git commit --fixup=293070e

Which will produce a commmit with a message of:

    fixup! Ensure new hotness works

A commit message formatted this way tells git-rebase (with `--autosquash`)
to fix the patch in this commit up into the commit with the message "Ensure
new hotness works". The power of using the commit message instead of SHA1
to identify commits is that this will work even after a rebase without
`--autosquash` (e.g. pulling in lastest master changes).

Here's how it would look in github:

{% img /images/autosquash/fourth_commit.png %}

*Obviously, don't have conversations with
yourself on github. This is purely educational ;)*

--------------

Now the fun part! When the pull request is approved, you can rebase with
autosquash (and interactive) and watch as git does the work for you:

    $ git rebase master -i --autosquash

Produces the rebase todo file:

    pick 293070e Ensure new hotness works
    fixup 3877fdf fixup! Ensure new hotness works
    pick e14aa92 Implement new hotness backend
    pick cdaa049 Add new hotness to UI

Simply save it and git rebases the branch as if you had changed the file
yourself. You can then merge and have a beer for all your efforts!

## Automating autosquash

Adding the long `--autosquash` flag all the time can get tiresome. Luckily,
you can add the `rebase.autosquash` config value to run autosquash
automatically for every interactive rebase.

    $ git config --global rebase.autosquash true

If no commits with the `fixup!` or `squash!` syntax are found, the rebase
continues normally. To override the autosquash default value, simply pass
the `--no-autosquash` flag to rebase.

Happy squashing!!

--Chris


