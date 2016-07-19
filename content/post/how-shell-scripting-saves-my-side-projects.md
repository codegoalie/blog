+++
date = "2016-07-19T17:58:03-04:00"
title = "How shell scripting saves my side projects"

categories = ["How To", "Self-Reference"]
description = "Use a deployment shell script to save headaches"

+++

I work on a lot of little side projects. Many of them are short-lived and small
scale. I start them to learn a new technology, to learn a new concept, try an
idea, or just to see if I can actually build something cool. I should also
mention that my memory is terrible. I "remember" things by figuring them out
again. Rote memorization is basically non-existent to me. I've recently come up
with a new best practice for my side projects which has saved my butt several
times now.

It's a `deploy.sh` script and I put one in every project that I do which needs
to be built, deployed, or executed beyond the typical compile step. This
very blog [has one](blog-deploy-dot-sh). There are also a few best practices
I've developed for making this file useful and not just another headache.

# Runable

This seems like a no-brainer, but hear me out. This file should be executable on
its own. It should not be `deploy.rb`. It should not need to be compiled or
otherwise prepared to run. You are writing a script. Script away all of that
tedium. If you need to deploy with ruby, make your `deploy.sh` simply contain
`ruby deploy.rb`. The point here is that you can `cd` into your project and run
this script. Period. If you have to remember to initialize your Python
virtualenv first, you've missed the point. Set it and forget it.

# Helpful

Not _everything_ can be scripted away. Sometimes a deploy requires some unique
information, such as an environment or version number. Every microservice I
create is meant to run in a [docker](docker) container on
[kubernetes](kubernetes). In order to automate building, tagging, pushing the
image, and then updating the deployment, the deploy script needs to know the
version number. Since I've deployed 10 times today to "fix" that one bug, I can
easily remember to pass the version to the script: `./deploy.sh v1.0.1337`.
However, I won't be so hip to that fact tomorrow. Good thing we are writing a 
script. Just add some checks and helpful error messages to guide your future
self down the right path. Here's an easy one for requiring an argument to
your script:

```
#!/bin/bash

if [ -z "$1" ]
then
  echo "Please provide a version number, like v35"
  exit 1
fi

# other deploy code here
```

It may seem like a drag, but you'll be so happy that you took the time to
take care of your own self now.

# Complete

Lastly, your deploy script needs to do every step on its own. It's a grown-up
script now and can handle it. If you need to do just one more thing after the
deploy finishes, you might as well just `rm deploy.sh`. Even steps which you
might consider "optional" now, __need__ to be included. For example, this blog
is [hosted on AWS S3](aws-s3-static) and CDN'ed by CloudFront. It really is
enough to only upload (read: sync; save those bits) the files. Eventually the
cache will expire and the new content will be shown. However, in just one more
line in the `deploy.sh`, I can invalidate the CloudFront distribution and see
this awesome new post right away. If you think it's optional, it's required.

Well, those are my three tips for keeping your side project deployments sane.

Happy deploying!!

__P.S.__ I've recently had a resurgence of shell scripting in general. In the
past, I've certainly been one to (ab)use 
[zsh's history substring search](sub-search) to re-run the same set of commands
over and again. See also: "Up 12 times then enter. 6 times." By committing those
mini-scripts to `~/bin/`, it really has made me much more efficient. A practical
example is streamlining my workflow at work. We use Github for code hosting and
reviews. We also use [YouTrack](youtrack) for our project management. I wrote a
[command line client for YouTrack](goutrack) and combined all the commands I was
doing to [checkout branches by story number](checkout-story) or create new
branches as well as marking stories In Progress/Under Review/etc. into shell
scripts like `review_story c-1234` or

```
$ start_story -t bug -s c-1234 -b this-is-a-heisenbug
Applying "Assignee: me In Progress" to story c-1234
Switched to new branch 'bugs/c-1234-this-is-a-heisenbug'
```

Get creative and really push yourself to save some time. Again, you'll thank
yourself, and then me. ;)


[blog-deploy-dot-sh]: https://github.com/chrismar035/blog/blob/master/deploy.sh
[docker]: https://www.docker.com
[kubernetes]: http://kubernetes.io
[aws-s3-static]: http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html
[youtrack]: https://www.jetbrains.com/youtrack/
[goutrack]: https://github.com/chrismar035/goutrack
[checkout-story]: https://github.com/chrismar035/dotfiles/blob/master/bin/git-checkout-story
