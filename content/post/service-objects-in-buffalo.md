+++
date = "2019-02-27T05:09:02-05:00"
title = "Service 'Objects' in Buffalo"
categories = ["Golang", "Buffalo"]
+++

For many recent projects, I've been using the excellent
[Buffalo](https://gobuffalo.io/en) web development eco-system. It's a great
collection of tools and packages for building web applications without needing
to reinvent the wheel for each app. In this post, I'll be highlighting a
technique I use based on the service object design pattern of abstracting
business logic from your applicaton implementation to increase readability and
reusability.

<!-- more -->

## But, why?

Here's a scenario I find myself in with increasing frequency. I've just
implemented some great new feature or process. It's good to go and super
helpful in its intended usage. All's good.

Then, you deiscover another, slightly different, use for the same feature. For
example, the system can send one-off reminder emails to individual users, but
now we want to remind all users. Or, I'd like to manually kick off that
background data integrity routine, but only for a single account and not the
entire user base. Or, I'd like to queue this process up in a background worker,
but only in certain cases.

There are proper extractions here for these exact scenarios. Typically, this is
the extract function or method refactoring step. We will talk about that in a
minute, but the first thing I want to address is the __where__ does that
abstraction live.

## A place for everything and everything in its place, until

The universal answer to almost any question in programming and software design
is "Sure, it could." For a certain case, almost any imaginable specific
solution approaches the ideal solution. Should this be a method on the model?
Sure, it could. Wouldn't this be better in the controller? Sure, it could. How
about we extract this into its own repo and it will live in a completely
separate open-source project? Sure, it could.

To combat this, I like to personify my functions, classes, and methods as super
lazy beings. They are constantly asking me, "Do I _have_ to do that?" and "What
if I don't want to know about all that?" I find this extremely helpful in
following the single responsibility principle and avoiding scope creep within
code constructs.

> Imagine your functions as super lazy people that don't want to do more than
> they absolutely _have_ to.

For example, my models don't like to send emails. My email sending functions
don't want to know about my user models, just email address strings. Route
handlers don't feel like learning SQL. You get the idea.

But (and there's always a but), sometimes there isn't a really good,
immediately known place to put some piece of logic. This is where the service
"object" pattern comes in. I almost think of it as a catch-all, last resort
solution to design questins. Will a service work best for you? Sure, it could.

## Ok what is it _exactly_

Hopefully by now, you're on board with at least the idea of using a service to
contain some kind of cross-cutting, or self-contained unit of logic.
Specifically, in `go` in the `Buffalo` world, what is a service?

I put services as exported functions in a `services` package. The directory
structure looks like this:

```diff
  actions/
  mailers/
  templates/
+ services/
+   notify_weekly_winner.go
```

And I implement one like this:


```go
// service/notify_weekly_winner.go
package services

// NotifyWeeklyWinner sends a congratulations notification to a weekly winner
func NotifyWeeklyWinner(email, firstName string, dogsWalked int) error {
  giftCardCode, _ := GetGiftCardForWalkingDogs(dogsWalked) // another service ;)

  return mailers.SendWeeklyWinnerEmail(email, firstName, giftCardCode)
}
```

I know what you're thinking: "Ok, this is a really simple example just to show
the concept. A real service would be way more complex, right?" Sure, it could. 
However, I think even this short example is actually very exemplary. Let's see
an alternative implementation and back into how we ended up here.

## Add to route handler (controller)

Probably the first implementation of this process was in a route handler
function (or controller) somewhere. Maybe there's a specific button in the
interface to notify a weekly winner which maps to a handler which does some
controller-y stuff (validates params, fetches data from DB, etc.), then has the
two lines from the service above, then redirects to another path.

```go
// actions/notifications.go

func notifyOfWinningHandler(c buffalo.Context) error {
  // load some models

  giftCardCode, _ := GetGiftCardForWalkingDogs(dogsWalked)
  // actually handle error

  err := mailers.SendWeeklyWinnerEmail(email, firstName, giftCardCode)
  if err != nil {
    // report error
    return errors.WithStack(err)
  }

  return c.Redirect(302, "/home")
}
```

Ok, actually seems reasonable. Could this be a better solution? Sure, it could.

So, time for a confession. I just made the above service example to show a
super simple example. I gave no thought to the rest of the application around
it or what it might even do. Now that we're stuck with it, let's take a second
to think about the world we've created.  

We know that every week we send a gift card to someone (with a first name and
an email address) who has walked some dogs. The amount of the card may be based
on the number of dogs walked. We've implemented some handler to send a
notification with the gift card code to such a person.

We do have some known unknowns though. We don't know what criteria constitutes
a winner. We don't know if there are one or multiple weekly winners. We don't
even know if this system has a `User` model. All that is a __great thing!__ We
don't need to know any of those things to send an email. Our implementation
doesn't need (or want) to know it either.

However, I'm not happy. Based on this handler, it would seem that someone
somewhere needs to click a link or button every week to notify the winner. We
can do better.

## Using a background worker

Let's say we don't trust humans and want to send the notification each week on
an automated schedule. Let's also say we have a background task system which
does this. Then we'd simply extract the logic into a worker.

```go
// actions/worker.go

var w worker.Worker

func init() {
  _ = w.Register("notify_weekly_winner", func(args worker.Args) error {
    // load from args, etc.

    giftCardCode, _ := GetGiftCardForWalkingDogs(dogsWalked)
    return mailers.SendWeeklyWinnerEmail(email, firstName, giftCardCode)
  })
}
```

The nice thing here is that we can also keep our handler, if we need a
manual fail-safe.

```go
// actions/notifications.go

func notifyOfWinningHandler(c buffalo.Context) error {
  // load some models

  _ = w.Perform(worker.Job{
    Handler: "notify_weekly_winner",
    Args: worker.Args{
      "firstName": firstName,
      "email": email,
      "dogsWalked": len(dogs),
    },
  })

  return c.Redirect(302, "/home")
}
```

This is fine. It's not very testable. Could it be justifed extracting to a
service just for better tesability? Sure, it could. You might also have a great
testing harness for background jobs and this isn't an issue. However, I'm going
to get a little hand wavy here with the specifics, but I find myself in the
below type of situation somewhat regulary. I bet you do too.

There's that random, one-off-that-becomes-semi-weekly, completely unanticipated
feature request. The CEO needs wants to send a gift card to his personal dog
walker who's not in the system. We want to back-fill the past 6 months of
winners that we tracked in a spreadsheet. This is where the rubber meets the road.

> The hallmark of a well designed sytem is its ability to handle unexpected change.

Using our service, we can easily add a grift task to send arbitrary notifications.

```go
// grifts/notify.go

var _ = grift.Namespace("noitfy", func() {
  grift.Desc("winner", "Send a gift card for walking dogs")
  grit.Add("winner", func(c *grift.Context) error {
    email := c.Args[0]
    firstName := c.Args[1]
    dogsWalked := c.Args[2]

    return service.NotifyWeeklyWinner(email, firstName, dogsWalked)
  })
})
```

Or we can upload a CSV to send notifications.

```go
// actions/upload.go

func uploadWinnersHandler(c buffalo.Context) error {
  // read from CSV

  for _, winner := range winners {
    service.NotifyWeeklyWinner(winner.Email, winner.FirstName, winner.DogsWalked)
  }

  return c.Redirect(302, "/home")
}
```

Thank you for taking this journey into service "objects" with me. As always,
please feel free to contact me with any questions, suggestions, criticisms, or
thoughts at chris@codegoalie.com.

-- Chris
