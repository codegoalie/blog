+++
date = "2026-04-18T05:54:21-04:00"
title = "Agents for System Design"
categories = ["AI", "system-design"]
draft = false
+++

System Design used to be reserved for the senior folks. They'll hand down a
document showcasing the new architecture or new service. Agents are making it so
everyone can do some system design because even the smallest features can
benefit from more intentional design.


<!--more-->

Over the past couple months, I've been tasked with leading a very large
cross-team project to essentially replace the core data model in our business.
This has involved designing new services, new and novel interactions between
services, and adding new capabilities to existing services. I've leaned heavily
on agents to help produce and communicate my intent to other people (and other
agents). Here is advice I've picked up along this journey.

## Know what you want

This is a general principle for all if not close to all interactions with an
agent and LLM. It's not a magic oracle, even if it genuinely feels like it
sometimes. It can't read your mind. It doesn't have the context of your company,
team, feature, past mistakes, etc. It wasn't at the last all-hands meeting to
absorb some of that new initiative from the leadership team. It wasn't a part of
that ad-hoc conversation last week where we got clarity on an upcoming API
interaction.

It doesn't need to know that. It shouldn't know that. It's your job to determine
what it should know, and in order to do that, you need to determine what you want
it to do first. Every time you open up your agent, you should know what you want
from it and when you'll be able to exit it (ctrl+d ctrl+d).

As a principal engineer at PrizePicks, a lot of my work is designing new
systems, adding new capabilities to existing systems, or integrating 2 systems
together. The first step that I take is to create a proposal doc. There is a lot
of formatting and process around this typically in companies. I ignore most of
that here. I want the agent to produce a document which describes at a high
level how this new thing is going to work.

That last sentence is pretty much the functional part of my initial prompt. The key
here is know what you want before you start:

- A document defining something in a 3rd party system (Notion, Linear docs,
  etc.)
- A series of steps for me to execute some task
- JSON for a grafana chart
- Mermaid diagram of this flow/architecture
- etc.

Have an end in mind before you start. Agents are a tool. Waving a shovel around
wildly in the air is not the best way to dig a hole.

## Provide the load bearing walls

This is a recent insight that I realized I'd been doing naturally, but I
articulated it to a colleague recently and it actually inspired this whole post.
This 5-second version is that if you're building a tent with the help of an
agent, you need to bring the tent poles. It can build the waterproof and
functional covering. It can put in a door with a 2 sided zipper. But if you
don't bring the poles, it'll just be a pile of fabric on the floor.

Conversely, you don't need to build the whole tent out. It knows what tents are
and how, generally, they work. It's your job to, first, communicate that you're
building a tent (these are general purpose models). And then articulate what
makes your tent yours.

A good recipe for this is to start with what you have. Talk about what you need.
Then be explicit about what you want. A while back, I had an agent research the
Epcot Flower & Garden festival menus for this year, comparing first a markdown
file then [a static HTML file](https://codegoalie.com/flower-2026.html). My wife
and I went through the menus and picked the items we wanted to be sure to try.
Now, I wanted to combine the two -- Well, wait. Here's the exact prompt I used:

```
❯ I have a full overview of the 2026 Epcot Flower & Garden festival in the
  2026.[md|html] files. I've gone through them and noted my favorites in
  2026-notes.md. I'd like to come up with a useful and intuitive guide to use
  while I'm in Epcot to make sure I don't miss these choices. We'll be going
  around the world showcase in one order or another so put the booths in the same
  order as the world showcase starting with Mexico. I also would love to be able
  to hide stuff I've already tried.
```

This was in plan mode in Claude Code so it generated a
[plan](/agents-for-system-design-plan-example.md).

## Meticulously review

Once you have a plan or document, it _needs_ your review. You've provided a few
sentences and it's generated a whole document. This upscaling of information is
lossy, **by definition**. In fact, each step of the way, you're going from lower
specificity to higher specificity and review is necessary.

The earlier steps need more review as they're setting the stage for everything
afterwards. A small misalignment in the initial plan will cascade and amplify
into the final product.

I once missed that a message topic needed to have a version bump. The agent used
`v1` in the plan, but we actually wanted `v2`. Even the copilot during code
review after I manually fixed the version numbers was complaining that "it
should be `v1` here."  😩

This ties directly into the first point in this post. Know what you want
beforehand so that you can evaluate it when the agent produces the artifact.

## Cutthroat revisions

Since each phase feeds directly into another increase in specificity, be
ruthless in your revisions earlier rather than later. I use the same working model as I
do for code reviews: if this isn't what you would have done, say something. It
will only get worse from here. The models are very good at making things sound
plausible and correct. That's exactly what they do, in fact. "The new
multiplication function can live in the addition package since they are both
math." Nope. Maybe you want to rename that package to newmath, or put
multiplication in its own package. You need to make the call now and update the
plan. It's a one sentence change in the plan, but from here on out it gets more
ingrained (maybe AGENTS.md updates to include something like "All math features
are implemented in the `addition` package" 😱)

Functionally, I like to have the agent make the changes usually in the same
conversation as the original plan was created. However, since you have an
artifact, you can start a new conversation if you want. That's the beauty of
working with artifacts outside of the harness.

----

I find the system design part of this new Agentic Engineering paradigm to be the
most interactive. Some days I like that. Other days I appreciate being able to
hit a button and get a PR (more on that later). But the PR button only works
when the plan is solid. I used to spend days hand-writing a technical design doc
and it was often just OK. With agents, I get really great docs in often less
than an hour of focused work after days of
[noodling](/posts/2025-05-24-use-your-noodler).

Happy designing!

 -- Chris
