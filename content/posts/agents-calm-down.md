+++
date = "2026-03-30T07:21:16-04:00"
title = "Agents Calm Down"
categories = ["AI", "Thoughts"]
+++

Agentic coding harnesses are violating the unix philosophy and trying to become
the _everything app_ for coding (and work and personal assistant and so on).

<!--more-->

## Why not build everything?

Many of the articles I'm reading are saying what we've been saying all along,
"writing the code hasn't been the bottleneck." No project was late because
engineers didn't spend enough time sitting at their desks typing code. And now
that writing the code is approaching zero, I think it's more important than ever
to carefully, methodically consider every project and initiative.

> "This feature is not a good fit for coding agents so we aren't going to put
> it into our harness."
>
> - No AI company ever

Non-engineering folks have long enjoyed the luxury of engineering being the
bottleneck (not writing code, but review, deploy, integration, etc.) and have
been able to change requirements, goals and targets while we were working. When
we can take a set of requirements and later that afternoon be dev complete...
Just think about what would have happened if we'd implemented verbatim some
of those first draft project proposals?

I'm working on a personal project to upgrade my personal daily task list from a
plain markdown file to use [Remember The Milk](https://www.rememberthemilk.com/)
(the only task tracking app which gets recurring items right, but I digress). I
have a pretty decent idea of what I want. I've been working in this flow for
over 8 years after all. I'm, of course, having an agent write all the code. But
I'm going slow. I'm carefully considering each feature and more precisely how it
should work than I ever have _ahead of time_ before. I feel this great
responsibility to move intentionally **because** I have this great power to push
a button, fold 5 pieces of clothes, turn back to my laptop and have a working
feature.

To me, LLMs and agents and all of it, from the start, has never been about
getting faster. It's about reducing the "manual" effort of willing a (software)
thing into existence. As I've been gaining experience with agents et al, I keep
coming back time and time again to the best practices of the industry: "have a
really good and detailed scope doc," "compare that to the code and form a
focused implementation plan," "break that down into units of work that depend on
each other or can be done in parallel." We always wanted that but it was too
time consuming to do and we relied on each other's existing context. Many
tickets don't have any body description. We just talked about the project scope
in the kick off, but didn't formalize a document. Ironically, the machine is
forcing (and enabling) us to do the things that would have been best all along,
even for humans.

## Do one thing well

Time and again the best software is focused and does one thing really well.
That's the unix philosophy. Composability over batteries included. Make a simple
and powerful tool to let those using it combine it with other simple and
powerful tools to make something greater than the sum of the tools themselves.

These new releases in the agent harnesses are hard to reason about because
many of the new features feel half-baked and not rooted in solving a real
problem. I end up feeling obligated to find use for them. It's FOMO a bit.
"Well, if they implemented it and released it, it must be something good. I must
be missing something if I can't find the use case."

It's hard to face this down. The company worth tens of billions of dollars is
churning out features on the most talked about software of the moment and my gut
is telling me to ignore most of it. I got bored and frustrated really quickly
babysitting the agent. "Yes" "Approve" over and over. Same prompt. Same slash
command. Same skill. Tweak it a bit here and there. Now, I'm automating it and
running into some longing for more focus on a simple tool that I can work _with_
not indefinitely inside of.

## Do less

I don't want to leave on a down note so let's talk solutions. Do less. Make
more. Let's build an ecosystem around this tool. Let's solve the rest of the
SDLC competently. LLMs are a versatile technology and are made even more
powerful with agent harnesses. They aren't a silver bullet either. I love that
we're pushing the envelope of what can these things do. I love that we don't
know yet. It's exciting to be a part of.

The more I work with agents the more I see how important the "old" best
practices are. The more pre-planning matters. The more detailed specs matter.
The more nailing down inter-service interacations matter. Start at the
boundaries and work inward on both sides. Hand offs. Metrics. Automated
end-to-end testing. There's nothing new here. It's just compressed and
accelerated; and can be exhausting at times. In this age where we can build
anything, the taste and discipline to not build something matters. I'd love to
see that in the tools themselves.

Happy shipping!

-- Chris
