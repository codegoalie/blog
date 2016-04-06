+++
date = "2016-04-06T23:04:17-04:00"
title = "Git References"
categories = ["git"]
+++

Everyone knows how to checkout a branch, `git checkout master`, or how to look
at a specific commit, `git show a1c8b6d`. But few know that branches, tags,
and commit SHAs are typically interchangeable in these and many other `git`
commands. Plus there is a whole set of modifiers to reference commits near to
specific commits. In this post, we'll explore all these techniques to become
expert `git` referencers.

<!-- more -->

# References

Below we will explore the different ways we can express a commit in `git`. While
each technique has its own strengths and weaknesses, being able to wield a lot
of `git`'s power and saving a lot of time comes from using these references
interchangeably.

## SHA1s

This first and most recognizable way to reference a commit is by its SHA1. This
is the full or part of the long random looking string of letters and numbers.
These are generated based on the contents of the commit, including current state
of the repo's files, commit message, author and committer, and timestamp. If any
of those items change, a new SHA1 will be generated. Here are some examples of
`git` commands using the SHA1.

```
git show abc123
git cherry-pick 321bca
git reset bbbaa4
```

## Branch Names

Branch names are also something that are a big part of a `git` workflow. Under
the hood, branch names are just aliases for commit SHA1s. Literally, you can see
the branch names in the `.git/refs/heads` directory of your repo. Each file
there contains one line which has the SHA1 of the commit it references. Here are
some common usages of branch names:

```
git checkout master
git rebase stable
git merge features/new-hottness
git cherry-pick bugs/broken-email-form
```

An important aspect of branch names is the commit they reference can change. For
example, when you create a new commit the branch which you are currently on
automatically gets updated to the new SHA1.

## Tags

Tags are very similar to branch names in that they are also friendlier aliases
for commit SHA1s. However, unlike branches, tags cannot be changed once created.
This makes them ideal for marking fixed, important commits in the history of
your code base. Releases and versions are a good usage for tags. Here are some
example commands using tags:

```
git tag v1.0.0
git checkout -b 1.1-backport v1.1.0
git show v0.9.0
```

## HEAD

The `HEAD` commit is the current tip of the branch you are on. Similar to the
`pwd` program, `HEAD` tells you where you are. On its own, the useful command is
`show` which will show you the details of the last commit you made.

# Modifiers

`git` also allows you to specify commits by their relation to other commits. In
the `git` data structure the only explicit relationship between commits is
child-parent. That is, the child commit knows its parent, but the parent does
not know its child/children. Many of the commands which show or span multiple
commits, such as `log` or `diff`, actually traverse the git tree to aggregate
their output.

## First Parent

The `~` modifier follows a references first parent. For example, `HEAD~`
references the first parent of the current commit. The first parent modifier can
be repeated: `HEAD~~` references the first parent of the first parent of the
current commit. Also, a number can be specified for many generations: `HEAD~5`
follows ancestors back 5 generations. Here are some other uses of the first
parent modifier:

```
// Move the second to last commit into the current branch
git cherry-pick bugs/broken-email-form~ 

// Modify some of the last 5 commits on your branch
git rebase HEAD~6

// Mark your current changes to fixup into two commits ago
git commit -a --fixup HEAD~
```

## Other Parents

Through merges, a commit can have multiple parents. The last modifier of the day
specifies any parent of a commit. The caret, `^`, modifies the reference to
follow its first parent; the same as '~'. However, specifying a number along
with the caret follows subsequent parent commits. For example, reference the
last commit of a branch before it was merged into the current branch with
`HEAD^2`.

# Bringing it all together

Any of the above references can be combined with any number of modifiers to
express the exact commit succinctly. Here are some examples:

```
// See the 3rd to last commit from the last branch merged to the stable branch
git show stable^2~~~

// Pull second to last commit from version 2 into your current branch
git cherry-pick v2.0.0~

// Create a new branch 2 commits back from a known SHA1
git checkout -b branch-from-history abcd122~~
```

The above examples might seem extremely specific, but knowing and using these
techniques can turn wasted time digging through git logs or copy and pasting
SHA1s into a quick one-liner. Impress your friends and co-workers, save your own
time, and begin thinking of your `git` history relatively.

Happy referencing!!

-- Chris
