+++
title = "Cleaning Up Docker Images"
date = "2019-12-30T16:13:36-05:00"
categories = ["docker"]
+++

After a while of using docker locally for development, you may notice that you
have a lot of images and containers laying around on your disk that you no
longer use. This post shows you an effective way to clean up 50 of GB or more
of disk space.

The first, best thing to do is clean up dangling images. These are docker images
that are not referenced by a container. These can be orphaned when containers are
removed or intermediate steps that don't get cleaned up. One quick command can
remove them:

```
$ docker image prune
```

Typically, if you've been using docker for a while, this will clear up quite a bit
of space. But, there's more we can do.

The next step you might think to do is remove other images that you know you don't use.
We can list them with the `docker images` command. However, you won't be able
to delete them directly because they are being referenced by containers (otherwise
they would have been removed by the prune command). So, let's look at containers:

```
$ docker ps -a
```

> Note: the `a` flag shows all containers not just those running. You probably
> don't want to remove a container that's currently running anyway.

Wow. That's a long list. Way down at the bottom I noticed some old and temporary
projects and experiments. Here's an example of some less notables from my list:

```
68585b76a752        46d00b64e6cb                                 "/bin/sh -c yarn"        13 months ago        Exited (1) 13 months ago                                   upbeat_tesla
3cb298f62318        3bc06921fcd0                                 "/bin/sh -c yarn"        14 months ago        Exited (1) 14 months ago                                   charming_benz
31e91aaa9111        3bc06921fcd0                                 "/bin/sh -c yarn"        14 months ago        Exited (1) 14 months ago                                   upbeat_lovelace
79428b687b22        6533ab88e0ff                                 "basj"                   16 months ago        Created                                                    welcomely_web_run_75
```

Ok, so now copy and paste the container ID (first column) for each one you... J/K.

I also noticed that this output has the created time in the fourth column. This
is helpful, but not particularly useful. I do have some long running projects
and would prefer not to simply remove containers that I've created long ago.

However, the very next column shows the last time the container was executed. I
would like to remove containers that I haven't run in a while. We can grep for
rows of the output which exited many months ago:

```
 $ docker ps -a | grep -E "Exited \([0-9]{1,3}\) 2[0-3] months ago"
```

This looks scary. But, I promise I actually wrote this by hand and it's pretty
simple. If I'm being honest, it's probably too simple, but it worked for my case.

First, we use the `E` flag to enable the regex engine. Then we want to match rows
with the string like "Existed (<some number>) <some number more than 20> months
ago". Most of that is plain strings. Really just for the numbers we want to use
the regex. The first is the exit code in the parenthesis. Most containers had
`0` or `1` exit codes. But, a few had `137`. So I just matched on any up to 3
digit number within the parenthesis: `[0-9]{1,3}`.

Second, we match a plain 2 then any units digit of months between 0 and 3,
inclusively: `2[0-3]`. My results had the oldest container stopping 23 months
ago. You mileage may vary and I'll leave it up to you to modify and re-run to
suit your situation.

Now that we've got a good list of containers to delete, let's use some
command-line fu to save a ton of copy/pasting. Let's pipe this filtered list
into `awk` to get rid of the rest of the text save for the first hash (field).

```
awk '{print $1}'
```

Then, pass each row (which now only contains the ID hash of the container) into
`docker rm`. To do this, we can use `xargs`:

```
xargs -i@ docker rm @
```

Putting it all together:

```
$ docker ps -a | grep -E "Exited \([0-9]{1,3}\) 2[0-3] months ago" | awk '{print $1}' | xargs -i@ docker rm @
```

Then, go back to the top and remove dangiling images:

```
$ docker image prune
```

There you have it. I removed containers I hadn't run for more than 8 months or so and freed up almost 50GB.
I hope you have similar or better results! Let me know how you fare: chris@codegoalie.com

Happy `docker rm`-ing!
