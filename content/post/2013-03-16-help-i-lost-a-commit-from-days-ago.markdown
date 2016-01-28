---
layout: post
title: "Help! I lost a commit from days ago!!!"
date: 2013-02-08
comments: true
categories:
  - git
  - HowTo
---

Oh no! I'm screwed! Better try to remember what work I did and recreate
it... :( J/K! This is git! Of course there's a slick way to recover what
you lost. Here's my situation: I was working on a feature branch happily
coding away. Finished the feature, rebased it quickly to fix a typo and
then merged it into master. All's well in my world. However, that was
days ago and today I just realized that I accidentally removed one of my
commits from the feature branch while I was working on it. No worries.
Here's how I got the commit back with relative ease.

<!--more-->

<a id='lg'></a>
First, let me give you a lay of the land. I use the incredible git lg alias.

    lg = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --

Seriously, steal that now. Use it a thousand times a day. I wish I
could attribute it to the original author, but I have since forgotten
where I originally saw it. At any rate, every few weeks I see it posted
anew on a different site.

Anyway, here's where I was at before the recovery:

{% gist 4738855 lost_commit.sh %}

Well...now what? Redo all that work in the lost commit. Nah. Reflog to the rescue! Git's <a href="http://www.kernel.org/pub/software/scm/git/docs/git-reflog.html">reflog</a> is a (by default) 90 day record of everywhere your HEAD ref was pointing. Anytime you do a checkout, create branch, commit, rebase; anytime the 'current' commit of your working directory changes, the reflog gets a new entry. You can think of the reflog as a record of what you've been doing. If you've had it in your working directory in the past 30 days, it's in the reflog.

Remember what the commit message was for my lost commit? Nice! We can easily grep for it:

    chrismar035:super_sweet_rails_app(master) $ git reflog | grep "commit message"

What's that? I didn't tell you the commit message for the lost commit? Well, I don't remember either! Now we are screwed. 

Gotcha again! We can still find it. We can use the ancient art of looking for what we lost. It's easy. Simply do a <code>git reflog</code> and you will see a list of everywhere you've been:

{% gist 4738855 reflog.sh %}

AHA! Not only did you find the <code>LOST COMMIT!!!</code>, but we can also look at what happened too. Apparently, on a mad dash to get the feature merged before going out and getting my drink on with some chaps, I accidentally rebased my commit right out of the project. Damnit.

Oh well, at least you found it for me. Thanks. Now, we've only got one real choice to fix this. We have to cherry-pick the commit out of the reflog back into master. Because I've already merged my feature branch into master and pushed it, I cannot go back and rebase or otherwise edit that pushed history of master. I've got to bite the bullet and add a commit straight onto master... Everyone screws up once in a while.

In the reflog, there are two ways to reference the commit: the SHA1 and the <code>HEAD@{integer}</code> reference. Either one will work. I like the SHA1 because I can double click in the terminal and it gets correctly highlighted for copying. Copy it and we'll paste it back into the command line with:

    chrismar035:super_sweet_rails_app(master) $ git cherry-pick 9a7de0e

`lg` that again and see how we look:

{% gist 4738855 all_fixed.sh %}

Nice! Now, notice that the SHA1 changed from what you copied out of the reflog. Remember, commit SHA1s are based on their content (files, dirs, commit messages and meta data) AND their parent(s). So, if you change the parent of the commit, you change the commit (Same reason all the SHA1s change when you rebase). In reality, the commit you cherry-picked is duplicated on to the branch you cherry-pick it into. However, in our case that's exactly what we wanted, because I messed up and deleted the commit in the first place.

Nice work! Push and have a beer!! :)

-- Chris
