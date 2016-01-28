---
layout: post
title: "Ruby on Rails/ActiveSupport: To delegate or not to delegate"
date: 2011-08-12
comments: true
categories: 
  - HowTo
  - Ruby On Rails
  - Self-Reference
---

This is an account of my adventure with delegation from problem to apparent solution to bug in ActiveSupport to you're doing it wrong! 

<!--more-->

<a href='#tldr'>TL;DR</a>

Delegation is used when you want to forward a method call from on class/model to an associated class/model. The <a href="http://guides.rubyonrails.org/active_support_core_extensions.html#method-delegation" title="Ruby on Rails Guide - Delegation">Ruby on Rails Guides</a> use the example of a User model which has a Profile associated with it. This is a great example with a little subtlety which I overlooked. If you aren't famaliar with delegation, go ahead and get yourself learned. I won't wait for you though. This is text just come back when you're up to speed.

<h3>The Setup</h3>
Let's say we've got a Rails app with Drivers and Trucks. On the show page for drivers, we show the truck number, if that driver is in a truck. Easy-peasy:

    # app/views/drivers/show.html.haml

    .truck_number
    -if @driver.truck
      = @driver.truck.number
    -else
      Not Driving any Truck

NBD. Here's our problem:

### The Problem

As when any good application which acts as a font-end for a database, we track history on all edits, etc. So, when we update the Driver in a Truck, we want to add history for the Truck and the Driver. If the Driver is already in another Truck we want to show, in his history, that he moved from Truck 1001 into Truck 2002. We'll say we have a create_history method included into our Entity classes whose declaration looks something like:

    def create_history(attribute, prev_value, new_value)
So, we want to call something like:

    @driver.create_history('Truck Number', @driver.truck.number, @new_truck.number)

Jackpot! Works perfectly. We get the old Truck number (1001) from the @driver instance and the new Truck number (2002) directly from the @truck instance. We are geniuses.
Hold the phone though. What if that Driver didn't have a previous truck... Spoiler Alert: <pre lang='ruby'>NoMethodError: undefined method 'number' for nil:NilClass</pre> I guess we could check that a Truck exists each time we want to access any attributes for Driver.truck. But, really, what do we expect Driver.truck.number to be if the Driver is not in a Truck? Nil would work...

### Delegate: for science!

I'll allow it. Let's delegate and allow_nil:

    # app/models/driver.rb

    class Driver < ActiveRecord::Model

      delegate :number, :to => :truck, :prefix => true, :allow_nil => true

      # ...

    end

Works! Now, we've got history showing: Driver had no Truck and moved 
into Truck 2002. Geniusness times 2. Delegation to perferction.

-----------------------

Sometime later...

Instead of the Truck number, maybe we want to store the id of the Truck 
in the history. Perhaps we know the truck number may change over time and want to link up the correct Truck record. Seems easy:

    delegate :id, to: :truck, prefix: true, allow_nil: true

But, when our Driver doesn't have a 'previous' truck:

    RuntimeError - Called id for nil, which would mistakenly be 4 -- if you really wanted the id of nil, use object_id

WTF? I allowed nil. I know he doesn't have a previous truck. I just want
my nil back and I'll go about my business. Let's get our hard hats on and
get digging into the source. I'll save you some googling and just tell
you that the Delegation module is in ActiveSupport in the Core Extensions
under Module. Scroll, scroll, scroll. There! Line 136! They(we)(whomever)
are only rescuing from NoMethodErrors. Calling id on nil raises a
RuntimeError, which isn't rescued and bubbles up to us. This is me
stomping my feet and wining. My knee jerk reaction was to just rescue
RuntimeErrors too:

    rescue NoMethodError, RuntimeError

### We're gonna be Famous

It works! AND, how cool are we? We get to submit a bug fix to Rails.
Uber-cool. Uh-oh, uneasyness...crap...
It just doesn't feel right to just catch any old RuntimeError and
possibly, silently fail to nil. However, the urge to try and submit a
simple 'fix' to Rails was strong. Instead, I started doing more research
into delegate and Ruby Exception handling. Here's what I've come up with:

<a name='tldr'></a>
### The Moral of the Story
You should delegate when you want to hide an architectural aspect and
expose the expected abstraction. In the Ruby on Rails Guides example,
we expect a user to have a name through @user.name even through name
actually resided in Profile. However, in our example, a Driver isn't
expected to have a truck_id. A truck has an id, but a driver does not
have a truck_id.

One of the classic 'bad smells' in code for refactoring is using a
temporary variable in place a a query. Ruby and its optional
parantheses, blurs the lines between variable, attribute and method.
It's easy to forget what you are doing and assume everything is an
attribute. Why shouldn't a Driver have a truck_id? The same reason a
Truck doesn't have a CDL. But, we can query the truck_id for the
kTruck associated with a Driver with a method.

After all that, I should have just written a query method in Driver as
such:

    def truck_id
      self.truck.id if self.truck
    end

Too easy...

**UPDATE 3/16/2013** 
>  As I convert this blog to Octopress and reread
>  these posts, I'm see some imporvements. Instead of the code above, the
>  `try` method is really what we want to use here:

>      def truck_id
>        self.truck.try(:id)
>      end

>  On `Object`, `try` will attempt to send the parameter as a message to
>  the invoking object. So, it works just like calling the method. However,
>  on `nil`, `try` simply returns `nil`. It effectively exactly replaces
>  the first implementation nicely.


-- Chris
