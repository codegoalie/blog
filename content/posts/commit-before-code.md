+++
date = "2020-06-26T06:43:29-04:00"
title = "Commit Before Code"
categories = ['git']
+++

I propose a case for writing all of your commit messages for a feature, bug,
pull request _before_ writing a single line of code and afterward not adding
any additional commits to your branch. Plan and execute. Give clarity and focus
to your reviewers. Here's how.

<!--more-->

This is an idea that's been floating around in my head for a while now:
pre-planning commits in your branches.  In fact, I checked my older posts
because I thought there might be a pretty good chance I had written this post
already. There wasn't. So, here it is.

## What am I talking about?

Making all your commits to complete your task _before_ you begin coding.
Literally using `--allow-empty` to outline all the tasks your branch needs to
do before you write one line of code. Every commit after that of code changes
are all `fixup` commits to one of the original commits. No new commits allowed.

## Why would anyone do that?

I find the exercise of planning my attack in the form of concrete commits
beneficial for __clarity__ and __focus__.

First, I can think abstractly about the work to be done. I don't know which
lines of code will change or even what they will change into, but rather, I can
focus solely on what those changes need to achieve.

I can think at a much higher level and coordinate the expected changes together
without getting bogged down by the intricacies or specific implementation
details. I don't need to think about error handling, variable naming, design
patterns, code smells, testability, etc. (unless any of those are core to the
rationale of the branch). It's almost a pure-er way of processing the task at
hand. I focus only on what are the smallest set of steps to reach the goal.

Secondly, and often more importantly, I force myself to remain focused on the
task at hand. If I make a change that doesn't fit into any of the predetermined
commits, there's a very good chance that the change doesn't belong in this
branch and should be made elsewhere.

Most often these are housekeeping tasks; small improvements to the code that I
happen to notice while doing something unrelated. Sometimes these are areas
that don't adhere to newly adopted best practices. Or, improvements in
readability. These aren't things that are critical, but help keep code quality
up over time. I'll get into what to do with these kinds of changes later.

## Ok, but how can I do this?

Let's take an example and build out our branch of empty commits. Imagine we're
working on an app to track vacations. We have an entity that holds our check-in
and check-out dates. What we want now is to display the number of days and
nights of the stay. For example, a stay from July 14th to 20th is 7 days/6
nights.

One thing to notice about this new feature is that the numbers are always one
off from each other. We can calculate one and then derive the other.

I like to write my tests first (in one commit) and then get them to pass in
another. I'll also prefix my test-only commits with "Ensure". Using this
pattern, I'd want to write test for and then implement the number of days
calculation. Then test and implement displaying to users. Here's the commands to
acheive this:

```sh
$ git commit --allow-empty -m "Ensure amount of days can be calculated from trips"
$ git commit --allow-empty -m "Calculate amount of days from trips"
$ git commit --allow-empty -m "Ensure users can see days/nights for a trip"
$ git commit --allow-empty -m "Display days/nights for trips"

```

Then after writing the tests for the calculation, I would create a `fixup`
commit to [autosquash][1] into the first commit from above:

```sh
$ git commit --fixup HEAD~~~ # using a relative commit reference
# or with the sha1 (prefix)
$ git commit --fixup 06aa143 
```

Learn more about [git references][2].

When all is said and done (or even before that), you can have git clean things
up for you with:

```sh
$ git rebase master --autosquash
```


## What about those small, unrelated changes?

These are changes I, personally, love to make. I believe this is where the
rubber meets the road in software as a craft. The holy trail of the huge
rewrite is often so tempting, but if you can't put new learnings or best
practices into existing code then how can you think that you'll be able to do
it in a brand new system. If you can prove that you are a good enough developer
to make the existing system its best, then you know you are ready to tackle a
rewrite. However, you also won't need to. ;)

So, what could be the harm of slipping in some minor improvements with your other
work? I'm already in here. Let's just fix it really quick. Well, this will get
you into trouble in at least 2 ways.

First, if the rest of your branch becomes obsolete or a better solution
arrives before you merge, the codebase doesn't get to benefit from your
unmerged, unrelated change. Or worse still, if your merged branch needs to be
reverted, you will also be reverting your unrelated change.

Secondly, it has a very real chance to hold up your PR during review. There's
no better way to almost guarantee a flame war than think you can squeeze in
a small, quick change. "Why is this fix here?" "If you're fixing this, why
didn't you fix that?" "You should fix it in this way instead.", etc. Your
2 second "improvement" will undoubedly attract comments and suggestions like
moths to a flame. The __actual__ point of the PR will be fine, but you'll get
stuck going around and around on your small addiiton.

## If you can't make these changes in your current branch, where do they go?

__TL;DR__ Move them into another branch and open a separate PR.

There are 2 ways to do this. One uses the stash and one uses commits and cherry
picking. I'll start with stash.

Use the [git-stash][3] to move changes across branches. The stash is a temporary
holding place for uncommitted changes. You can stash these changes on one branch
and apply them to another. I'll assume you've committed all changes with fixups
and want to move all uncommitted changes to another branch.

```sh
$ git stash save
$ git checkout master
$ git checkout -b a-good-name-for-changes
$ git stash pop
$ git add .
$ git commit
$ git push
```

I always prefer `git stash pop` to `git stash apply` because the former removes
the stash entry when applying it and keeps your stash clean. Once it's applied
and committed, you no longer need that stash and there's no sense in keeping it
around.

Now, for the second way. This way is a little less dangerous since you always
have your changes committed, but maybe only by a hair. Here you'll commit to
your working branch. Then create a new branch and cherry pick that commit into
the new branch. This technique also works will if your "small" fix has multiple
commits.

```sh
$ git commit
[commit-before-code e4fe22f] Prefer single quoted strings
 1 file changed, 3 insertions(+), 3 deletions(-)
$ git checkout master
$ git checkout -b string-style-fixes
$ git cherry-pick e4fe22f
$ git push
```

> ProTip: `cherry-pick` takes any git commit reference. Utilize the branch name
> to cherry pick the tip of that branch into your current branch.

The really cool thing about this method is that if your fix branch gets merged
before your feature branch, you can simply rebase on master (which you should be
doing anyway) and git will detect the duplicate changes and automatically remove
the cherry picked commit.

-----------

Next time you are starting to work on a new branch, give this method a try and
see if it helps keep you clear on your objective and focused on nailing it.

Let me know how it works out for you.

Happy committing!

&mdash; Chris


[1]: https://codegoalie.com/2013/04/04/better-pull-requests-with-git-autosquash
[2]: https://codegoalie.com/2016/04/06/git-references
[3]: https://git-scm.com/docs/git-stash
