+++
date = "2018-01-12T08:20:15-05:00"
title = "Ruby refactoring: Open/Closed Principle"
categories = ["Ruby", "Reactoring"]
+++

Let's examine a refactoring to move code to follow the
[open/closed principle](https://en.wikipedia.org/wiki/Open/closed_principle).
We'll see how the resulting calling code becomes much easier to read locally,
without having to open other files or classes to understand what's going on.

<!-- more -->

## Open/closed principle

First, let's do a quick recap of the open/closed principle. Classes should be
open to extension, but closed to modification. What does that mean? Let's take
it a half at a time.

"Classes should be open to extension." This means building
your classes in a way that they are simple and single-use enough to be reusable
or combine-able. This is the difference between building a Lego brick and a
fully built spaceship. The spaceship is more complete, but when you're tired of
playing spaceships, you can't easily reconfigure it into something else.

Second, "classes should be closed to modification." Violating this
principle will require you to modify far off code to implement your current
feature. You should structure your code to avoid this because you may forget
to change that far off code, other developers on the team may not know to change
that code, and it's often a mystery why this far off code is even related.
More practically, this often manifests in a list of classes, types, "allowed"
things, "blacklisted" stuff, etc. If you add a new class and then have to add
that class to a list somewhere, you're probably not following open/closed.

## Sending update notifications

I recently had a project where we wanted to send some update notifications to
users when entities they were interested in were updated by other users. This
Rails application exposes a JSON API and has a bulk update mechanism. The 
controller action which handles these bulk requests is generic such that many
types of models can be updated simultaneously. After successful updates, we
schedule a background job to send the update notifications:

```ruby
if entity.save
  SendUpdateNotificationJob.perform_later(entity)
  ...
end
```

Initially we only sent updates for new or updated Posts:

```ruby
class SendUpdateNotificationJob < ApplicationJob
  def perform(entity)
    return unless entity.class == Post
    
    # send push notifications here
  end
end
```

## Adding more notification types

Seems reasonable enough. However, new and updated post notifications were such
a hit that when we added responses to the application, people asked to get
updates for them as well. Super easy to do that:

```diff
- return unless entity.class == Post
+ return unless entity.class == Post || entitty.class == Response
 
```

And then bulletins

```diff
- return unless entity.class == Post || entitty.class == Response
+ return if entity.class == Post || entitty.class == Response || entitty.class == Bulletin
 
```

Your level of pain tolerance may vary, but to me, this is already __way__ out
of control. Even though we aren't expressing it as an array or list explicitly,
we are building up a list of classes which we decided earler was a sign of
violating open/closed.

## Naming conditionals

So, how do we fix this? A really nice refactoring technique I like to use is
what I call "naming conditionals" (super trademarked;
[not to be used without express written consent of Ricky Bobby, inc.](https://www.youtube.com/watch?v=Md1MDHroXGU)).
This is pretty easy to do. I take a conditional, extact it to a method and
give it a name. Let's do that here:

```ruby
def ______?(entity)
  entity.class == Post || entitty.class == Response || entitty.class == Bulletin
end

```

Now the hardest part of programming: naming this method. I like to keep it
simple, so how about `send_updates?`? Now our calling code reads like this:

```ruby
class SendUpdateNotificationJob < ApplicationJob
  def perform(entity)
    return unless send_updates?(entity)
    
    # send push notifications here
  end

  def send_updates?(entity)
    entity.class == Post || entitty.class == Response || entitty.class == Bulletin
  end
end
```

The calling code is much easier to read: Don't send updates unless you should.

_But_, we haven't solved the open/closed problem yet.

## Reverse dependency injection

One of my favorite discussions in programming is about who doesn't care about
things. In this case, I would say that this job does not care about which
classes the entities are that it gets. It only cares about if it can send
notifications for them, and then doing so. In this case, it would not check
the classes of the entity.

If tho doesn't know about the classes, then who does?  Well, the entities know
their classes. What if the job asked them if updates should be sent for
themselves?

Then we'd have code like:

```ruby
class SendUpdateNotificationJob < ApplicationJob
  def perform(entity)
    return unless entity.send_updates?
    
    # send push notifications here
  end
```

That seems pretty straightforward to me.

> Quick aside: It might also be worth removing that conditional from the job
> and preforming the check before even scheduling the background job. This would
> allow you to send notifications for "unallowed" types if really necessary but
> put the gate keeping burden upon the scheduler of the job. Trade-offs...

## Set a default, override when necessary

With Rails 5+, the concept of an `ApplicationRecord` was introduced to give a
single parent class for your models within your application. This is a great
place to add code or configuration to be shared by all models.

For most models, we don't want to send updates:

```ruby
class ApplicationRecord < ActiveRecord::Base
  ...

  def send_updates?
    false
  end
end
```

Any class we want to send updates for can say so:

```ruby
class Post
  ...

  def send_updates?
    true
  end
end
```

Now, we don't ever have to _open_ the send updates job and add more classes to
the list. When we add `NewsArtlcles` next month, it'll be super straightforward
to allow or disallow notifications for them. Further, we can add more logic in
the `send_updates?` method; like only sending updates bulletin created after
2pm on a Sunday.

If you find yourself adding and removing from lists of classes in your
application, take a moment to think about the open/closed principle and
whether or not it can help you make more readable, modifiable, and exemplary
code.

Happy open/closing!

-- Chris
