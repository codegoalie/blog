+++
categories = ["Containers", "Kubernetes", "Docker"]
date = "2016-02-04T15:11:50-05:00"
description = ""
slug = ""
tags = []
title = "Working with Containers: beyond the tutorial"

+++

Over the past few months, I've been getting my hands dirty with containers,
Docker, and Kubernetes in an effort to get some hands on experience working
toward microservices. I've been building up a small application to generate and
serve Sudoku puzzles. My original goal was to see how many puzzles with unique 
solution I could actually find, but that's another post entirely. There are
already
[many](https://docs.docker.com/engine/userguide/basics/)
[great](http://kubernetes.io/v1.1/examples/guestbook-go/README.html)
[tutorials](https://cloud.google.com/container-engine/docs/tutorials/guestbook)
about
[Docker](https://docs.docker.com/)
and
[Kubernetes](http://kubernetes.io/v1.1/docs/whatisk8s.html)
on [Google Container Engine](https://cloud.google.com/container-engine/docs/),
so I won't go into getting started details here. This post is meant to explain
some of the stickier points that I had to pickup the hard way. I hope to save
you one or two headaches.

## Docker 102

Just Google "Docker getting started" and you'll be inundated with step by step
tutorials building a generic image. Those are all very helpful getting a handle
on the Docker tooling, but after that there seems to be a dead end.  I found a
really complicated way to print to the console but I was left saying, "What
now?" A really simple way to get some use out of Docker right away, without a
complicated cloud setup, is creating a development environment for your
application.

A great benefit here is that you don't need to install all of the dependencies
(libraries, databases, etc.) on your machine. How many times have you gone back
to an old project 6 or more months later only to find it no longer runs because
it needs some old version of something? Think of Docker as a wrapper keeping
things inside self-contained and unaffected by the outside world and not
subject to bit rot.

Another point about development environments, feel free to go against the
"Docker Best Practices" for images when starting out. You don't have to get the
benefit of running your production image in development from day 1. Dump
everything into the image. You can always split things apart later and use
Docker Compose to bring multiple images up at once.

## Turn Key Kubernetes

Typically, I've used AWS for my infrastructure needs, but Google Container
Engine runs kubernetes for you and can spin up a new cluster with one command.
Again, there are many tutorials about the specifics but here are a few things I
didn't know going in which would have been helpful.

### Keeping costs down

By default your cluster is composed of 3 `n1-standard-1` instances. When just
getting started this is probably more than you need in both resources and cost.
Since I was more interested in playing with containers than messing with
compute engine instances (that's the whole point of containers), I didn't pay
any attention to them, but you should. It's super easy and quick to change both
the number of instances and the instance types in your cluster.

Google Container Engine clusters are built on the idea of [instance
groups](https://cloud.google.com/compute/docs/instance-groups/), which
are just one or more instance defined by the same [instance
template](https://cloud.google.com/compute/docs/instance-templates). The
template described the instances you want in your group with attributes like 
machine type and base image, etc.  In the Google Cloud Console, you can design
a new template right in the interface (pick a new machine type from a drop down)
and use smaller or larger instances. 

Scaling the number of instances in your cluster is even easier. Edit the
Instance Group and change the "Number of Instances" textbox value. You can even
enter 0 to stop getting billed for the instance time. This works great when you
don't need the instances to be up 24/7 while just playing around.

### Persistent Storage

When a pod is restarted or rescheduled, it gets recreated from scratch. Anything
that was stored on disk is gone. This can cause unexpected issues. For example,
I was using redis for storing Sudoku puzzles and if the redis-master pod
restarted, I lost all contents of the database. This can be unexpected because
when running redis locally, the disk snapshots always remain even when
restarting the redis-server process. With containers, this is not the case. If
you need to store anything to disk that you care about, you'll need to store
that in a volume backed by a Google Persistent Disk. Once again, there are many
tutorials on the specifics.

### Stuck in CreatingContainer

When using a Google persistent disks, I was running into pods getting
rescheduled onto new nodes (instance), but the disk remained attached to the
previous node. Since Google Cloud persistent disks can only be attached to one
node at a time, this caused the pod to hang during creation and never start.
The quick fix to this is just detach the disk from it's current node.
Kubernetes will attach it to the correct node for you.

```
gcloud compute instances detach-disk <instance-name> --disk <disk-name>
```

There's currently an effort to redesign the volumne mount/dismount system in
Kubernetes to address this issue. I also think that as redis was maxing out the
memory on the nodes and crashing, it was causing unnecessary havok on my 
cluster.

## "Restarting" a pod

Early on my Sudoku generator was very naive and had exponention performance, so
it would get "stuck" trying to come up with new puzzles. Locally, I was just
restarting the process. But when I got it into the cluster, it wasn't always
clear if it was broken, or just getting held up (I did fix this and went from
a puzzle every few minutes to a few puzzles a second). The great feature of
using replication controllers is that it will keep the specified number of pods
running. So to "restart" a pod that's being managed by a replication controller,
just delete it. The replication controller will bring up a new one. If you
aren't using a replication controller to manage your pods, do so.

Hopefully these tips will make your container journey a little smoother.
