---
categories:
- git
comments: true
date: 2013-02-26
layout: post
title: Oh my! What large hot fixes you have
---

We've all been there: just finished a nice new feature, deployed it out
to production only to find that you've completely overlooked an edge
case or use case which is now totally breaking your app. Sometimes you
have to push a big hot fix. It has to get in immediately. It can't wait
for writing correct tests or other better abstractions and
implementations. What to do? What to do?

<!--more-->

Well, there's the common way of hacking as fast as you can until you're
pretty sure the bug is fixed, commit everything in a big "Avert
crisis!!" commit. However, I think we can do better.

First step checkout a new branch at your current 'production,' or
similar. Call it production_pre_fix. Don't check it out or work on it,
just leave it there as a placeholder.

    $ git checkout production
    $ git branch production_pre_fix

Now for the fun part: hack away! But, follow your usual development
practices of committing early and often. Refactor a method. Commit.
Add some if checks for edge cases. Commit. Get the shit fixed and
deployed. Go on. I'll wait.

Ok, alarms are quiet now and you're done breaking shit? Good. Now
let's get to work on the real fix. I'm glad your hacked together bunch
of duct tape fix is holding, but let's not leave things like that. I
know you and I bet you've got some good work there. You probably don't
want to just throw it all away. That's cool. Why don't we use the duct
tape as a basis for the permanent fix? Here's how:

First, get a clean branch off master

    $ git checkout master
    $ git checkout -b bugs/prod_fix

Then, write tests to account for your new found bugs.

Next, cherry pick your current fix onto this branch.

    $ git cherry-pick production_pre_fix..production

You may have noticed I passed two branch names with two periods in between to cherry-pick. What the fuck, right? Well, as we all know, two commit SHA1s separated by two periods is a range of commits. For exmple, <code>2e45f..34b79</code>. You are saying that you'd like to use all the commits starting at <code>34b79</code> and following parent links back until you reach <code>2e45f</code>. 

But I've used brach names here, which are just human friendly shortcuts
for SHA1s. Remember branch names are basically pointers to a particular
commit. They can be used in any git command which would otherwise take
a commit SHA1. Add that to the fact that cherry-pick can take a range
and suddenly your doing some pretty powerful stuff with a pretty simple
command. Go you!

Now a little housekeeping,

* Make sure your fix actually passes your tests.
* Refactor and make your fix nice. Rebase, as necessary.
* Start pull request and get the feature merged back into master.


Then we need to reset your temp fix in production. Like this:

    $ git checkout production
    $ git reset --hard production_pre_fix
    $ git branch -d production_pre_fix
    $ git push -f

Woah woah woah! No, I didn't. I just force pushed a non-topic branch.
Isn't that a big no-no? Usually, yes and I would expect to be taken out
back and beaten until I learned my lesson. However, until I'm told of
a good reason otherwise: production or other released branches are not
shared among developers. They are an exact representation of what is
to be deployed next to the environment they represent.

Why aren't release branches an accurate representation of what is
currently deployed to the environment they represent? Because if you
want to know that, look at the environment. There's no need for
duplicate information. A branch like production should be curated and
hold what will be deployed next to production. You might not do that
curating and updating until moments before the deploy. But for all
that time until you deploy, if you had to emergency deploy, whatever
is in the branch will be deployed.

Back to business, we've reset production back to not include the duct
tape. Now it's time to merge master and our fix up to it.

    $ git checkout production
    $ git merge master

Congratulations! You've not only saved your company from sure collapse
by fixing a huge production bug. But you've also reconciled your
technical debt and prevented other developers behind you from cursing
your name at the duct tape-y hacks you introduced to the code base.
That deserves a beer!

-- Chris
