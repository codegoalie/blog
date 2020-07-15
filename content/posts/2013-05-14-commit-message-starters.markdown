---
categories:
- git
comments: true
date: 2013-05-14
layout: post
title: Commit Message Starters
---

As I've been working in git and crafting my commits with rebase
working toward creating pull requests which are easy to read,
review, and comment, I've been noticing myself fall into
habits of naming commit messages similarly which contain code to
acheive similar ends. Further, when I struggle to find the correct
words for a commit message, it's often easier to being with
a familiar word to get things flowing.

{% img right /images/readthesource.jpg 460 276 Read the source %}
Over the past few months, I've also had the pleasure of working
with some great developers. As such, I've been afforded the
opportunity to review a lot of their code. If there is one thing I recommend
to all developers, from novice to expert, it's ***read code***.
Your own, your friend's, strangers, projects you admire, anything you can get
your hands on.
Not only will it enlighten you to how others write code, new coding patterns
and syntax, but it will empower you to be able to figure out how the code you
use works and how to fix it.

As a quick aside, I was able recently to dig into the Ruby source code, even
into the C, to discover exaclty what was happening with Range bracket
operator access on an empty Array. It felt great to be able to see how Ruby
herself was implemented and know exactly why my code worked; to go beyond "well,
it worked in irb so it must be correct."

The great thing about reviewing pull requests is that I am able to open
discussions with the authors and inquire as to why they made certain decisions
and what their motiviations were for writing certain code. Also, it gave me a
chance to see code which was not polished and final. Thereby, recognizing
anti-patterns and less than best practices.

Coming back to the topic of this post. These anti-patterns and less than best-
practices extend to commit messages as well. Below I've listed some of the dos
and don'ts which I have started to use in my everyday committing.

<!-- more -->

## What I like

These words I often use to start commit messages which make some common
changes in the codebase.

### Ensure

    Ensure phone numbers strip extraneous characters

    Ensure deactivation resets users' api tokens

I use "Ensure" to start a commit which contains tests for my code. These commits
are often the first commits in a pull request, especially if I am using TDD. A
whole commit just for test? Surely, that's overkill? There are two reasons I
like to encapsulate tests into their own commits.

{% img left /images/ensure.jpg Ensure %} First, this standardization allows
others to know which commits will define
and test the behavior I aim to implement. We all know that tests can be a great
documentation tool and prefixing commit messages which contain "Ensure" allow
people to find them easier.

Second, if the tests are in their own commit(s) *before* the implementation
commits, it's very easy for a reviewer to simulate the red-green test cycle.
Either through a `checkout` or selecting a commit to be 'editied' in an
interactive rebase, the state of the repo *after* the tests are written, but
*before* the task is implemented can be recreated. Tests are run at that point
and a reviewer can cofirm that the new tests do indeed fail. The rebase is
continued and the tests can be run again. This time they succeed. A review has
very simply been able to confirm that the tests are working correctly.


### Boyscout

    Boyscout the user model specs

    Boyscout line lengths in the sessions controller

Boyscouting refers to updating the format and/or style of code without changing
the behavior. I picked it up from a presentation about code styles which I now
cannot find to reference here. However, I did find this
[written reference](http://www.cimgf.com/zds-code-style-guide/) online.
The term refers to a famous quote by the founder of the Boyscouts,
Robert Stephenson Smyth Baden-Powell,
["Try and leave this world a little better than you found
it"](http://www.scouting.org/scoutsource/CubScouts/Parents/About/history.aspx).

Continuing to think of the reviewer when committing, just by looking at the
message, expectations are set that this commit does not change functionality,
only formatting. Review of a change like that is much easier when you know that
nothing is supposed to happen.

### Migrate

    Migrate a unique index for user email addresses

    Migrate timestamp columns onto the comments table

As you might have guessed, I use "Migrate" to start commit messages which
contain migrations. As a best practice, we like to isolate migrations to their
own commits containing only the migration class definition and the changes to
the schema file. It also can be useful, but not 100% reliable, to quickly see
if a particular set of commits has migrations; say before a deploy or after
pulling down the latest changes. Again, along the theme of setting expectations
for others.


## What I avoid

These words often start a commit message off on the wrong foot. Being very
generic on their own, they often lead to very generic commit messages.

### Fixed

    Fixed broken specs

    Fixed editing a user

{% img right /images/fixedit.jpg FIXED!!! %}
First off, past tense should be avoided in commit messages. The rule of thumb
is to write a commit message as if you were commanding the code to take an
action. Secondly, commit messages should describe the reason for a change, not
the change itself. If someone would like a know what the changes were, they
need to do no more that a `git show` or click in github. However, to reason
why the change was made or what it is attempting to do is much harder to
determine from the code itself. Great commit messages can be the difference
between `Fixed broken specs` and `Activate users after registration in user
specs`.

### Added

    Added new Order model

    Added full_name method to User model

"Added" is not strictly a not so best practice, but I see it go awry more often
than I see it used for good. Again, "added" has a great tendnecy to lean toward
*what* happened instead of *why* did it happen. I, myself, sometimes write a
commit starting with "added". For example, `Added jquery javascript library`
at first glance seems perfectly reasonable. I didn't fix anything. I didn't
write a great new feature. I just added jQuery. However, when I find myself
with a commit message like this, I go through the practice of adding "in order
to" and then trying to finish the commit message. `Added jquery javascript
library` in order to `provide DOM manipulation methods`. Put it
together for `Provide DOM manipulation methods with jQuery`. Now, I've given
some context to why I added jQuery instead of simply restating the code changes
in the commit message.


That's all I have for now. Please comment below with your commit message best
practices and tendencies. I bet you guys have some great tips too!

See ya soon and keep committing!

--Chris
